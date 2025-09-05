import { AdminLayout } from '@/widgets/admin-layout';
import { Box } from '@/shared/ui/box';
import { Button } from '@/shared/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/shared/ui/avatar';
import { PageHeader } from '@/shared/ui/page-header';
import { IconButton } from '@/shared/ui/icon-button';
import { AdminIcon, AddIcon } from '@/shared/ui/icons';

export default function AdminUsersPage() {
  return (
    <AdminLayout>
      <div className="space-y-6">
        <PageHeader
          icon={<AdminIcon size={24} />}
          iconClassName="bg-red-500/15 text-red-600 dark:bg-red-500/20 dark:text-red-400"
          title="Users Management"
          description="Manage user accounts, permissions and access control"
          actions={
            <IconButton
              icon={<AddIcon size={16} />}
              variant="success"
              responsive
            >
              Add User
            </IconButton>
          }
        />

        {/* Users List */}
        <Box size="lg">
          <div className="space-y-4">
            <h2 className="text-xl font-semibold mb-4">All Users</h2>
            
            {/* Sample Users */}
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src="" alt="John Doe" />
                    <AvatarFallback />
                  </Avatar>
                  <div>
                    <h3 className="font-medium">John Doe</h3>
                    <p className="text-sm text-muted-foreground">john@example.com • Admin</p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">Edit</Button>
                  <Button variant="destructive" size="sm">Ban</Button>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src="" alt="Jane Smith" />
                    <AvatarFallback />
                  </Avatar>
                  <div>
                    <h3 className="font-medium">Jane Smith</h3>
                    <p className="text-sm text-muted-foreground">jane@example.com • Editor</p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">Edit</Button>
                  <Button variant="destructive" size="sm">Ban</Button>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src="" alt="Mike Wilson" />
                    <AvatarFallback />
                  </Avatar>
                  <div>
                    <h3 className="font-medium">Mike Wilson</h3>
                    <p className="text-sm text-muted-foreground">mike@example.com • User</p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">Edit</Button>
                  <Button variant="destructive" size="sm">Ban</Button>
                </div>
              </div>
            </div>
          </div>
        </Box>
      </div>
    </AdminLayout>
  );
}