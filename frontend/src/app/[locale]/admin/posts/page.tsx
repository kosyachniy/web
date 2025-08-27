import { AdminLayout } from '@/widgets/admin-layout';
import { Card } from '@/shared/ui/card';
import { Button } from '@/shared/ui/button';

export default function AdminPostsPage() {
  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">Posts Management</h1>
          <Button>Add Post</Button>
        </div>

        {/* Posts List */}
        <Card className="p-6">
          <div className="space-y-4">
            <h2 className="text-xl font-semibold mb-4">All Posts</h2>
            
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
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">Edit</Button>
                  <Button variant="destructive" size="sm">Delete</Button>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                  <div>
                    <h3 className="font-medium">Machine Learning Basics</h3>
                    <p className="text-sm text-muted-foreground">Science • Draft</p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">Edit</Button>
                  <Button variant="destructive" size="sm">Delete</Button>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div>
                    <h3 className="font-medium">Business Strategies 2024</h3>
                    <p className="text-sm text-muted-foreground">Business • Published 1 week ago</p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">Edit</Button>
                  <Button variant="destructive" size="sm">Delete</Button>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </AdminLayout>
  );
}