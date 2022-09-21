import { MailerService } from '@nestjs-modules/mailer';
import { Injectable } from '@nestjs/common';
import { SentMessageInfo } from 'nodemailer';
import { anyObject } from '../common/types';

@Injectable()
export class MailService {
	constructor(private readonly mailerService: MailerService) {}

	sendHtml(to: string, subject: string, template: string, context: anyObject): Promise<SentMessageInfo> {
		return this.mailerService.sendMail({
			to,
			// from: 'noreply@nestjs.com',
			subject,
			template: __dirname + `/${template}`, // The `.pug`, `.ejs` or `.hbs` extension is appended automatically.
			context,
		});
	}

	sendPlain(to: string, subject: string, message: string): Promise<SentMessageInfo> {
		return this.mailerService.sendMail({
			to,
			// from: 'noreply@nestjs.com',
			subject,
			text: message,
		});
	}
}
