import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PassportStrategy } from '@nestjs/passport';
import { Request } from 'express';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { JWT_COOKIE_NAME, JWT_STRATEGY_NAME } from '../../common/constants';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy, JWT_STRATEGY_NAME) {
	constructor(
		configService: ConfigService,
		private prismaService: PrismaService,
	) {
		super({
			jwtFromRequest: ExtractJwt.fromExtractors([JwtStrategy.extractJWTFromCookie]),
			secretOrKey: configService.get<string>('JWT_SECRET'),
		});
	}

	async validate(payload: any) {
		const user = await this.prismaService.user.findUnique({
			where: { id: payload.sub },
		});

		return user;
	}

	private static extractJWTFromCookie(req: Request): string | null {
		if (req.cookies && req.cookies[JWT_COOKIE_NAME] && req.cookies[JWT_COOKIE_NAME].length > 0) {
			return req.cookies[JWT_COOKIE_NAME];
		}

		return null;
	}
}
