'use client';

import { useTranslations } from 'next-intl';
import { SidebarCard } from '@/shared/ui/sidebar-card';
import { Button } from '@/shared/ui/button';
import { 
  BuildingIcon,
  BoxIcon,
  PhoneIcon,
  UsersIcon,
  CalendarIcon,
  HandshakeIcon,
  ChartIcon,
  BullhornIcon,
  DollarIcon,
  QuestionIcon
} from '@/shared/ui/icons';

interface SectionsSidebarProps {
  className?: string;
  title?: string;
  icon?: React.ReactNode;
}

export default function SectionsSidebar({ className, title, icon }: SectionsSidebarProps) {
  const tBusiness = useTranslations('businessSections');

  const sections = [
    {
      key: 'companies',
      label: tBusiness('companies'),
      icon: <BuildingIcon size={20} />
    },
    {
      key: 'products',
      label: tBusiness('products'),
      icon: <BoxIcon size={20} />
    },
    {
      key: 'contacts',
      label: tBusiness('contacts'),
      icon: <PhoneIcon size={20} />
    },
    {
      key: 'customers',
      label: tBusiness('customers'),
      icon: <UsersIcon size={20} />
    },
    {
      key: 'calendar',
      label: tBusiness('calendar'),
      icon: <CalendarIcon size={20} />
    },
    {
      key: 'sales',
      label: tBusiness('sales'),
      icon: <HandshakeIcon size={20} />
    },
    {
      key: 'analytics',
      label: tBusiness('analytics'),
      icon: <ChartIcon size={20} />
    },
    {
      key: 'promos',
      label: tBusiness('promos'),
      icon: <BullhornIcon size={20} />
    },
    {
      key: 'pays',
      label: tBusiness('pays'),
      icon: <DollarIcon size={20} />
    },
    {
      key: 'support',
      label: tBusiness('support'),
      icon: <QuestionIcon size={20} />
    }
  ];

  return (
    <SidebarCard 
      title={title}
      icon={icon}
      className={className}
      contentSpacing="sm"
    >
      <div className="space-y-1">
        {sections.map((section) => (
          <Button
            key={section.key}
            variant="ghost"
            className="w-full justify-start gap-3 hover:bg-muted"
          >
            {section.icon}
            {section.label}
          </Button>
        ))}
      </div>
    </SidebarCard>
  );
}