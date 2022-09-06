import {
  ConflictException,
  ForbiddenException,
  Injectable,
  InternalServerErrorException,
  Logger,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';
import { PrismaClientKnownRequestError } from '@prisma/client/runtime';
import * as argon from 'argon2';
import { PrismaService } from '../prisma/prisma.service';
import { AuthDto } from './dto';

@Injectable()
export class AuthService {
  private logger = new Logger('AuthService');

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
    } catch (error) {
      if (error instanceof PrismaClientKnownRequestError) {
        // The .code property can be accessed in a type-safe manner
        if (error.code === 'P2002') {
          throw new ConflictException(
            'Email taken, a new user cannot be created with this email',
          );
        }
      }

      this.logger.error(error.message, error.stack);
      throw new InternalServerErrorException(
        'Something went wrong, try again later',
      );
    }
  }

  async signIn(authDto: AuthDto) {
    const user = await this.prismaService.user.findFirst({
      where: { email: authDto.email },
    });

    if (!user) {
      throw new ForbiddenException('Credentials is incorrect');
    }

    const pwMatch = await argon.verify(user.password, authDto.password);

    if (!pwMatch) {
      throw new ForbiddenException('Credentials is incorrect');
    }

    delete user.password;

    return this.signToken(user.id, user.email);
  }

  async signToken(userId: number, email: string) {
    const paylaod = {
      sub: userId,
      email,
    };

    const secret = this.configService.get<string>('JWT_SECRET');

    const token = await this.jwtService.signAsync(paylaod, {
      expiresIn: '90d',
      secret,
    });

    return {
      access_token: token,
    };
  }
}
