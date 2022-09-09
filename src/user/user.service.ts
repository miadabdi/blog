import { Injectable, Logger } from '@nestjs/common';
import { User } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { UpdateUserDto } from './dto';

@Injectable()
export class UserService {
  private readonly logger = new Logger(UserService.name);

  constructor(private prismaService: PrismaService) {}

  async updateUser(updateUserDto: UpdateUserDto, user: User) {
    const updatedUser = await this.prismaService.user.update({
      where: { id: user.id },
      data: updateUserDto,
    });

    delete updatedUser.password;

    return updatedUser;
  }
}
