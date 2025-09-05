import { AdminLayout } from '@/widgets/admin-layout';
import { Box } from '@/shared/ui/box';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { PageHeader } from '@/shared/ui/page-header';
import { PostsIcon, AddIcon, EditIcon, DeleteIcon } from '@/shared/ui/icons';

export default function AdminPostsPage() {
  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <PageHeader
          icon={<PostsIcon size={24} />}
          iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400"
          title="Posts Management"
          description="Create, edit and manage all website posts"
          actions={
            <IconButton
              icon={<AddIcon size={16} />}
              variant="success"
              responsive
            >
              Add Post
            </IconButton>
          }
        />

        {/* Posts List */}
        <Box>
          <div className="space-y-2">
            
            {/* Sample Posts */}
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div>
                    <h3 className="font-medium">Introduction to React 19</h3>
                    <p className="text-sm text-muted-foreground">Technology • Published 2 days ago</p>
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
              
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                  <div>
                    <h3 className="font-medium">Machine Learning Basics</h3>
                    <p className="text-sm text-muted-foreground">Science • Draft</p>
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

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div>
                    <h3 className="font-medium">Business Strategies 2024</h3>
                    <p className="text-sm text-muted-foreground">Business • Published 1 week ago</p>
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
          </div>
        </Box>
      </div>
    </AdminLayout>
  );
}