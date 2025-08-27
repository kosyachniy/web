import { AdminLayout } from '@/widgets/admin-layout';
import { Card } from '@/shared/ui/card';
import { Button } from '@/shared/ui/button';
import { Avatar, AvatarFallback } from '@/shared/ui/avatar';

export default function AdminUsersPage() {
  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">Users Management</h1>
          <Button>Add User</Button>
        </div>

        {/* Users List */}
        <Card className="p-6">
          <div className="space-y-4">
            <h2 className="text-xl font-semibold mb-4">All Users</h2>
            
            {/* Sample Users */}
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <Avatar className="h-8 w-8">
                    <AvatarFallback>JD</AvatarFallback>
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
                    <AvatarFallback>JS</AvatarFallback>
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
                    <AvatarFallback>MW</AvatarFallback>
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
        </Card>
      </div>
    </AdminLayout>
  );
}