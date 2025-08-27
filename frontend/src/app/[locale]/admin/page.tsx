import { AdminLayout } from '@/widgets/admin-layout';
import { Card } from '@/shared/ui/card';

export default function AdminPage() {
  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Welcome Section */}
        <Card className="p-6">
          <h1 className="text-3xl font-bold mb-4">Admin Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome to the admin panel. Use the sidebar to navigate between different sections.
          </p>
        </Card>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-4">
            <h3 className="font-semibold text-lg mb-2">Categories</h3>
            <p className="text-2xl font-bold text-primary">12</p>
            <p className="text-sm text-muted-foreground">Total categories</p>
          </Card>
          
          <Card className="p-4">
            <h3 className="font-semibold text-lg mb-2">Posts</h3>
            <p className="text-2xl font-bold text-primary">847</p>
            <p className="text-sm text-muted-foreground">Published posts</p>
          </Card>
          
          <Card className="p-4">
            <h3 className="font-semibold text-lg mb-2">Users</h3>
            <p className="text-2xl font-bold text-primary">1,234</p>
            <p className="text-sm text-muted-foreground">Registered users</p>
          </Card>
        </div>

        {/* Recent Activity */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between py-2 border-b">
              <div>
                <p className="font-medium">New post published</p>
                <p className="text-sm text-muted-foreground">Technology category</p>
              </div>
              <span className="text-sm text-muted-foreground">2 hours ago</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b">
              <div>
                <p className="font-medium">User registered</p>
                <p className="text-sm text-muted-foreground">john@example.com</p>
              </div>
              <span className="text-sm text-muted-foreground">4 hours ago</span>
            </div>
            <div className="flex items-center justify-between py-2">
              <div>
                <p className="font-medium">Category updated</p>
                <p className="text-sm text-muted-foreground">Science category</p>
              </div>
              <span className="text-sm text-muted-foreground">1 day ago</span>
            </div>
          </div>
        </Card>
      </div>
    </AdminLayout>
  );
}