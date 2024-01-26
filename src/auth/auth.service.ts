import {
	ConflictException,
	ForbiddenException,
	Injectable,
	InternalServerErrorException,
	Logger,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';
import { PrismaClientKnownRequestError } from '@prisma/client/runtime/library';
import * as argon from 'argon2';
import { Response } from 'express';
import { JWT_COOKIE_NAME } from '../common/constants';
import { PrismaService } from '../prisma/prisma.service';
import { AuthDto } from './dto';

@Injectable()
export class AuthService {
	private readonly logger = new Logger(AuthService.name);

	constructor(
		private prismaService: PrismaService,
		private jwtService: JwtService,
		private configService: ConfigService,
	) {}

	async signUp(authDto: AuthDto) {
		const hash = await argon.hash(authDto.password);

		try {
			const user = await this.prismaService.user.create({
				data: { email: authDto.email, password: hash },
			});
			delete user.password;

			return user;
		} catch (error: unknown) {
			if (error instanceof PrismaClientKnownRequestError) {
				// The .code property can be accessed in a type-safe manner
				if (error.code === 'P2002') {
					throw new ConflictException('Email taken, a new user cannot be created with this email');
				}
			}

			if (error instanceof Error) {
				this.logger.error(error.message, error.stack);
			}
			throw new InternalServerErrorException('Something went wrong, try again later');
		}
	}

	async signIn(response: Response, authDto: AuthDto) {
		const user = await this.prismaService.user.findFirst({
			where: { email: { equals: authDto.email, mode: 'insensitive' } },
		});

		if (!user) {
			throw new ForbiddenException('Credentials is incorrect');
		}

		const pwMatch = await argon.verify(user.password, authDto.password);

		if (!pwMatch) {
			throw new ForbiddenException('Credentials is incorrect');
		}

		delete user.password;

		const jwtCookie = await this.signToken(user.id, user.email);
		const cookieExpiresIn = this.configService.get<number>('COOKIE_EXPIRES_IN');

		response.cookie(JWT_COOKIE_NAME, jwtCookie, {
			expires: new Date(new Date().getTime() + cookieExpiresIn * 1000 * 60 * 60 * 24),
			sameSite: 'strict',
			httpOnly: true,
		});
	}

	async signToken(userId: number, email: string) {
		const paylaod = {
			sub: userId,
			email,
		};

		const secret = this.configService.get<string>('JWT_SECRET');
		const jwtExpiresIn = this.configService.get<string>('JWT_EXPIRES_IN');

		const token = await this.jwtService.signAsync(paylaod, {
			expiresIn: `${jwtExpiresIn}d`,
			secret,
		});

		return token;
	}
}
