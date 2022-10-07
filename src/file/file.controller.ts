import { Controller, Post, UploadedFile, UseInterceptors } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { FileService } from './file.service';

@Controller('file')
export class FileController {
	constructor(private fileService: FileService) {}

	@Post('upload-image')
	@UseInterceptors(FileInterceptor('image'))
	async uploadImage(@UploadedFile() image: Express.Multer.File) {
		return this.fileService.uploadImage(image);
	}
}
