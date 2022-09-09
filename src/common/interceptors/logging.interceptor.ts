import {
  CallHandler,
  ExecutionContext,
  Injectable,
  Logger,
  NestInterceptor,
} from '@nestjs/common';
import { User } from '@prisma/client';
import { Request } from 'express';
import { Observable } from 'rxjs';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  private readonly logger = new Logger(LoggingInterceptor.name);

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const ctx = context.switchToHttp();
    const request = ctx.getRequest<Request>();
    // const response = ctx.getResponse<Response>();

    const user = request.user as User | null;
    this.logger.verbose(
      `Calling ${request.originalUrl} \n with body ${JSON.stringify(
        request.body,
      )} \n and user id ${user?.id}`,
    );

    return next.handle();
  }
}
