import { ArgumentsHost, Catch, HttpException, Logger } from '@nestjs/common';
import { BaseExceptionFilter } from '@nestjs/core';
import { User } from '@prisma/client';
import { Request } from 'express';

@Catch()
export class AllExceptionsFilter extends BaseExceptionFilter {
	private readonly logger = new Logger(AllExceptionsFilter.name);

	catch(exception: unknown, host: ArgumentsHost) {
		if (!(exception instanceof HttpException) && exception instanceof Error) {
			const ctx = host.switchToHttp();
			// const response = ctx.getResponse<Response>();
			const request = ctx.getRequest<Request>();
			// const status = exception.getStatus();
			const user = request.user as User | null;

			const errorMessage = `${exception.message} \nCalling ${
				request.originalUrl
			}\n with body ${JSON.stringify(request.body)}\n and user id ${user?.id}`;

			this.logger.error(errorMessage, exception.stack);
		}

		super.catch(exception, host);
	}
}
