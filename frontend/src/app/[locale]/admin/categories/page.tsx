import { AdminLayout } from '@/widgets/admin-layout';
import { Card } from '@/shared/ui/card';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { PageHeader } from '@/shared/ui/page-header';
import { CategoriesIcon, AddIcon, EditIcon, DeleteIcon } from '@/shared/ui/icons';

export default function AdminCategoriesPage() {
  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <PageHeader
          icon={<CategoriesIcon size={24} />}
          iconClassName="bg-indigo-500/15 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400"
          title="Categories Management"
          description="Manage and organize your website categories"
          actions={
            <IconButton
              icon={<AddIcon size={16} />}
              variant="success"
              responsive
            >
              Add Category
            </IconButton>
          }
        />

        {/* Categories List */}
        <Card>
          <div className="space-y-2">
              <div className="flex items-center justify-between p-3 border rounded-[0.75rem]">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div>
                    <h3 className="font-medium">Technology</h3>
                    <p className="text-sm text-muted-foreground">12 posts</p>
                  </div>
                </div>
                <ButtonGroup>
                  <IconButton 
                    variant="outline" 
                    size="sm"
                    icon={<EditIcon size={12} />}
                    responsive
                  >
                    Edit
                  </IconButton>
                  <IconButton 
                    variant="destructive" 
                    size="sm"
                    icon={<DeleteIcon size={12} />}
                    responsive
                  >
                    Delete
                  </IconButton>
                </ButtonGroup>
              </div>
              
              <div className="flex items-center justify-between p-3 border rounded-[0.75rem]">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div>
                    <h3 className="font-medium">Science</h3>
                    <p className="text-sm text-muted-foreground">8 posts</p>
                  </div>
                </div>
                <ButtonGroup>
                  <IconButton 
                    variant="outline" 
                    size="sm"
                    icon={<EditIcon size={12} />}
                    responsive
                  >
                    Edit
                  </IconButton>
                  <IconButton 
                    variant="destructive" 
                    size="sm"
                    icon={<DeleteIcon size={12} />}
                    responsive
                  >
                    Delete
                  </IconButton>
                </ButtonGroup>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-[0.75rem]">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                  <div>
                    <h3 className="font-medium">Business</h3>
                    <p className="text-sm text-muted-foreground">15 posts</p>
                  </div>
                </div>
                <ButtonGroup>
                  <IconButton 
                    variant="outline" 
                    size="sm"
                    icon={<EditIcon size={12} />}
                    responsive
                  >
                    Edit
                  </IconButton>
                  <IconButton 
                    variant="destructive" 
                    size="sm"
                    icon={<DeleteIcon size={12} />}
                    responsive
                  >
                    Delete
                  </IconButton>
                </ButtonGroup>
              </div>
          </div>
        </Card>
      </div>
    </AdminLayout>
  );
}