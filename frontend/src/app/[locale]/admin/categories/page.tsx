import { AdminLayout } from '@/widgets/admin-layout';
import { PageHeader } from '@/shared/ui/page-header';
import { CategoriesIcon } from '@/shared/ui/icons';
import { CategoryManagement } from '@/widgets/category-management';

export default function AdminCategoriesPage() {
  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <PageHeader
          icon={<CategoriesIcon size={24} />}
          iconClassName="bg-indigo-500/15 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400"
          title="Categories Management"
          description="Manage and organize your website categories with nested hierarchy, custom icons, colors, and images"
        />

        {/* Categories Management */}
        <CategoryManagement />
      </div>
    </AdminLayout>
  );
}