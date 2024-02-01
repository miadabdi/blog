import { ArgumentsHost, Catch, HttpException, HttpStatus, Logger } from '@nestjs/common';
import { BaseExceptionFilter } from '@nestjs/core';
import { Prisma, User } from '@prisma/client';
import { Request, Response } from 'express';

export const errorMappings: Record<string, { status: number; message: string }> = {
	P2000: { status: HttpStatus.BAD_REQUEST, message: 'Input Data is too long' },
	P2001: { status: HttpStatus.NO_CONTENT, message: 'Record does not exist' },
	P2002: { status: HttpStatus.CONFLICT, message: 'Reference Data already exists' },
};

@Catch(Prisma.PrismaClientKnownRequestError)
export class PrismaClientExceptionFilter extends BaseExceptionFilter {
	private readonly logger = new Logger(PrismaClientExceptionFilter.name);

	catch(exception: Prisma.PrismaClientKnownRequestError, host: ArgumentsHost) {
		const ctx = host.switchToHttp();
		const response = ctx.getResponse<Response>();
		const request = ctx.getRequest<Request>();

		const errorCode = exception.code;
		const errorMapping = errorMappings[errorCode];

		const user = request.user as User | null;

		if (errorMapping) {
			const { status, message } = errorMapping;

			const errorMessage = `${exception.message} \nCalling ${
				request.originalUrl
			}\n with body ${JSON.stringify(request.body)}\n and user id ${user?.id}`;

			this.logger.error(errorMessage, exception.stack);

			response.status(status).json({
				statusCode: status,
				message: `${message} at path: ${
					request.originalUrl.split('/')[request.originalUrl.split('/').length - 1]
				}, Error Code: ${errorCode}`,
			});
		} else {
			exception instanceof HttpException ? exception.getStatus() : HttpStatus.INTERNAL_SERVER_ERROR;
			super.catch(exception, host); // Handle unknown error codes
		}
	}
}
