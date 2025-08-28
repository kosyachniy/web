'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { Box } from '@/shared/ui/box';
import { Input } from '@/shared/ui/input';
import { Textarea } from '@/shared/ui/textarea';
import { IconButton } from '@/shared/ui/icon-button';
import { 
  MailIcon,
  SendIcon
} from '@/shared/ui/icons';

interface ContactFormSidebarProps {
  className?: string;
}

export default function ContactFormSidebar({ className }: ContactFormSidebarProps) {
  const t = useTranslations('contact');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    console.log('Contact form submitted:', { email, message });
    // Reset form
    setEmail('');
    setMessage('');
  };

  return (
    <Box size="default" className={className}>
      <div className="space-y-4">
        <div className="flex items-center gap-2 mb-4">
          <MailIcon size={20} />
          <h3 className="font-semibold text-lg">{t('contactUs')}</h3>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="contact-email" className="text-sm font-medium">
              {t('email')}
            </label>
            <Input
              id="contact-email"
              type="email"
              placeholder={t('emailPlaceholder')}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="contact-message" className="text-sm font-medium">
              {t('message')}
            </label>
            <Textarea
              id="contact-message"
              placeholder={t('messagePlaceholder')}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={4}
              required
            />
          </div>

          <IconButton
            type="submit"
            icon={<SendIcon size={16} />}
            variant="default"
            className="w-full"
            disabled={!email || !message}
            responsive
          >
            {t('sendMessage')}
          </IconButton>
        </form>

        {/* Quick Contact Info */}
        <div className="pt-4 border-t space-y-2">
          <h4 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
            {t('quickContact')}
          </h4>
          <div className="text-sm space-y-1">
            <p className="text-muted-foreground">{t('emailUs')}: contact@example.com</p>
            <p className="text-muted-foreground">{t('callUs')}: +1 (555) 123-4567</p>
          </div>
        </div>
      </div>
    </Box>
  );
}