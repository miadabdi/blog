import { ForbiddenError } from '@casl/ability';
import { ForbiddenException, Inject, Injectable, Logger, NotFoundException } from '@nestjs/common';
import { User } from '@prisma/client';
import { CaslAbilityFactory, CaslAction } from '../casl/casl-ability.factory';
import { PRISMA_INJECTION_TOKEN } from '../prisma/prisma.module';
import { PrismaService } from '../prisma/prisma.service';
import { CreateTagDto, DeleteTagDto, GetTagDto, UpdateTagDto } from './dto';
import { GetTagsByIdDto } from './dto/get-tags-by-id.dto';

@Injectable()
export class TagService {
	private readonly logger = new Logger(TagService.name);

	constructor(
		@Inject(PRISMA_INJECTION_TOKEN) private prismaService: PrismaService,
		private caslAbilityFactory: CaslAbilityFactory,
	) {}

	async getTagsById(getTagsByIdDto: GetTagsByIdDto) {
		const tags = await this.prismaService.tag.findMany({
			where: {
				id: {
					in: getTagsByIdDto.ids,
				},
			},
		});

		return tags;
	}

	async createTag(createTagDto: CreateTagDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Create, 'Tag');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		const tag = await this.prismaService.tag.create({
			data: {
				name: createTagDto.name,
			},
		});

		return tag;
	}

	async updateTag(updateTagDto: UpdateTagDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Update, 'Tag');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		const tag = await this.prismaService.tag.findUnique({ where: { id: updateTagDto.id } });

		if (!tag) throw new NotFoundException('Tag not found');

		const updatedTag = await this.prismaService.tag.update({
			where: { id: updateTagDto.id },
			data: updateTagDto,
		});

		return updatedTag;
	}

	async deleteTag(deleteTagDto: DeleteTagDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Delete, 'Tag');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		const tag = await this.prismaService.tag.findUnique({ where: { id: deleteTagDto.id } });

		if (!tag) throw new NotFoundException('Tag not found');

		await this.prismaService.tag.delete({
			where: { id: deleteTagDto.id },
		});

		return 'ok';
	}

	async getTag(getTagDto: GetTagDto) {
		const tags = await this.prismaService.tag.findMany({
			where: {
				name: {
					contains: getTagDto.name,
				},
			},
		});

		return tags;
	}
}
