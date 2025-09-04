'use client';

import { useTranslations } from 'next-intl';
import { Logo } from '@/shared/components/layout';
import { ThemeSwitcher } from '@/shared/components/layout';
import LanguageSwitcher from '@/features/navigation/components/LanguageSwitcher';
import {
  TelegramIcon,
  TiktokIcon,
  YoutubeIcon,
  InstagramIcon,
  VkIcon,
  TwitterXIcon,
  FacebookIcon,
  LinkedinIcon,
  CopyrightIcon,
  LegalIcon,
  FaqIcon,
  CompanyIcon,
  MailIcon,
  HandshakeIcon
} from '@/shared/ui/icons';

const currentYear = new Date().getFullYear();

const socialLinks = [
  { name: 'Telegram', icon: TelegramIcon, url: '#', color: 'bg-blue-500/15 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400' },
  { name: 'TikTok', icon: TiktokIcon, url: '#', color: 'bg-pink-500/15 text-pink-600 dark:bg-pink-500/20 dark:text-pink-400' },
  { name: 'YouTube', icon: YoutubeIcon, url: '#', color: 'bg-red-500/15 text-red-600 dark:bg-red-500/20 dark:text-red-400' },
  { name: 'Instagram', icon: InstagramIcon, url: '#', color: 'bg-gradient-to-br from-purple-600 via-pink-600 to-orange-600 text-white' },
  { name: 'VK', icon: VkIcon, url: '#', color: 'bg-blue-600/15 text-blue-700 dark:bg-blue-600/20 dark:text-blue-300' },
  { name: 'X', icon: TwitterXIcon, url: '#', color: 'bg-gray-500/15 text-gray-600 dark:bg-gray-500/20 dark:text-gray-400' },
  { name: 'Facebook', icon: FacebookIcon, url: '#', color: 'bg-blue-700/15 text-blue-700 dark:bg-blue-700/20 dark:text-blue-300' },
  { name: 'LinkedIn', icon: LinkedinIcon, url: '#', color: 'bg-blue-800/15 text-blue-800 dark:bg-blue-800/20 dark:text-blue-200' },
];

export function Footer() {
  const t = useTranslations('footer');
  const tBrand = useTranslations('brand');
  const tSystem = useTranslations('system');

  return (
    <footer className="bg-background border-t">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
          
          {/* Brand & Rights Column */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Logo />
            </div>
            <p className="text-sm text-muted-foreground">
              {tBrand('description')}
            </p>
            <div className="flex items-center space-x-1 text-sm text-muted-foreground">
              <div className="bg-muted text-muted-foreground w-5 h-5 rounded-[0.75rem] flex items-center justify-center">
                <CopyrightIcon size={12} />
              </div>
              <span>{currentYear} {t('rights')}</span>
            </div>
          </div>

          {/* Legal Documents Column */}
          <div className="space-y-4">
            <h3 className="font-semibold flex items-center gap-2">
              <div className="bg-red-500/15 text-red-600 dark:bg-red-500/20 dark:text-red-400 w-6 h-6 rounded-[0.75rem] flex items-center justify-center">
                <LegalIcon size={14} />
              </div>
              {tSystem('privacy')}
            </h3>
            <nav className="flex flex-col space-y-2">
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {tSystem('privacy')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {tSystem('offer')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {tSystem('permission')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {t('rules')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {t('codex')}
              </a>
            </nav>
          </div>

          {/* Company Info Column */}
          <div className="space-y-4">
            <h3 className="font-semibold flex items-center gap-2">
              <div className="bg-blue-500/15 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400 w-6 h-6 rounded-[0.75rem] flex items-center justify-center">
                <CompanyIcon size={14} />
              </div>
              {t('about')}
            </h3>
            <nav className="flex flex-col space-y-2">
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer flex items-center gap-2">
                <MailIcon size={12} />
                {t('contacts')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer flex items-center gap-2">
                <HandshakeIcon size={12} />
                {tSystem('offer')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer flex items-center gap-2">
                <CompanyIcon size={12} />
                {t('jobs')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer flex items-center gap-2">
                <HandshakeIcon size={12} />
                {t('partners')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {t('white_paper')}
              </a>
            </nav>
          </div>

          {/* FAQ & Support Column */}
          <div className="space-y-4">
            <h3 className="font-semibold flex items-center gap-2">
              <div className="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400 w-6 h-6 rounded-[0.75rem] flex items-center justify-center">
                <FaqIcon size={14} />
              </div>
              {t('faqSupport')}
            </h3>
            <nav className="flex flex-col space-y-2">
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {t('faq')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {t('feedback')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {tSystem('rates')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {tSystem('refund')}
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                {t('news')}
              </a>
            </nav>
          </div>
        </div>

        {/* Social Media Section */}
        <div className="border-t pt-8 mb-8">
          <h4 className="font-medium mb-4 text-center">{t('followUs')}</h4>
          <div className="flex justify-center items-center gap-3 flex-wrap">
            {socialLinks.map(({ name, icon: IconComponent, url, color }) => (
              <a
                key={name}
                href={url}
                className={`w-10 h-10 rounded-[0.75rem] flex items-center justify-center transition-all duration-200 hover:scale-110 cursor-pointer ${color}`}
                title={name}
              >
                <IconComponent size={18} />
              </a>
            ))}
          </div>
        </div>

        {/* Bottom Section with Controls */}
        <div className="border-t pt-8">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            {/* Left: Brand Address */}
            <div className="text-sm text-muted-foreground">
              <span>{tBrand('address')}</span>
            </div>

            {/* Right: Theme & Language Switchers */}
            <div className="flex items-center gap-3">
              <ThemeSwitcher />
              <LanguageSwitcher />
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}