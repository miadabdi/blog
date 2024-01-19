import { Injectable, Logger } from '@nestjs/common';
import { BUCKET_NAMES_TYPE } from '../common/constants';
import { MinioClientService } from '../minio-client/minio-client.service';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class FileService {
	private logger = new Logger(FileService.name);

	constructor(
		private minioClientService: MinioClientService,
		private prismaService: PrismaService,
	) {}

	async upload(file: Express.Multer.File, directory: string, bucketName: BUCKET_NAMES_TYPE) {
		const result = await this.minioClientService.putObject(file, directory, bucketName);

		const fileRecord = await this.prismaService.file.create({
			data: {
				bucketName: result.bucketName,
				path: result.path,
				sizeInByte: result.size,
				mimetype: result.mimetype,
			},
		});

		return fileRecord;
	}

	async uploadImage(image: Express.Multer.File) {
		return this.upload(image, '', 'images');
	}
}
