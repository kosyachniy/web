import { getTranslations } from 'next-intl/server';
import { Metadata } from 'next';
import { PageHeader } from '@/shared/ui/page-header';
import { SpaceIcon } from '@/shared/ui/icons';

export async function generateMetadata(): Promise<Metadata> {
    const t = await getTranslations('navigation');
    
    return {
        title: `${t('space')} - Collaboration Tools`,
        description: 'Interactive spaces for collaboration and real-time communication',
    };
}

export default async function SpacePage() {
    const t = await getTranslations('navigation');

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-6xl mx-auto">
                    <PageHeader
                        icon={<SpaceIcon size={24} />}
                        iconClassName="bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400"
                        title={t('space')}
                        description="Common spaces for user interaction, collaboration, and real-time communication."
                    />

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Whiteboard */}
                        <div className="bg-card rounded-lg border p-6">
                            <div className="flex items-center mb-4">
                                <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
                                    <span className="text-2xl">📋</span>
                                </div>
                                <div>
                                    <h3 className="text-xl font-semibold">Whiteboard</h3>
                                    <p className="text-muted-foreground">Collaborative drawing and planning</p>
                                </div>
                            </div>
                            <p className="text-muted-foreground mb-4">
                                Share ideas visually with real-time collaborative whiteboard. Perfect for brainstorming sessions and project planning.
                            </p>
                            <div className="bg-muted rounded p-3 text-sm text-muted-foreground">
                                Coming soon: Real-time collaboration tools
                            </div>
                        </div>

                        {/* Video Chat */}
                        <div className="bg-card rounded-lg border p-6">
                            <div className="flex items-center mb-4">
                                <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mr-4">
                                    <span className="text-2xl">📹</span>
                                </div>
                                <div>
                                    <h3 className="text-xl font-semibold">Video Chat</h3>
                                    <p className="text-muted-foreground">Face-to-face communication</p>
                                </div>
                            </div>
                            <p className="text-muted-foreground mb-4">
                                Connect with team members through high-quality video calls with screen sharing capabilities.
                            </p>
                            <div className="bg-muted rounded p-3 text-sm text-muted-foreground">
                                Coming soon: Video conferencing integration
                            </div>
                        </div>

                        {/* Messenger */}
                        <div className="bg-card rounded-lg border p-6">
                            <div className="flex items-center mb-4">
                                <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mr-4">
                                    <span className="text-2xl">💬</span>
                                </div>
                                <div>
                                    <h3 className="text-xl font-semibold">Messenger</h3>
                                    <p className="text-muted-foreground">Instant messaging and chat</p>
                                </div>
                            </div>
                            <p className="text-muted-foreground mb-4">
                                Real-time messaging with file sharing, emoji reactions, and group conversations.
                            </p>
                            <div className="bg-muted rounded p-3 text-sm text-muted-foreground">
                                Coming soon: Real-time messaging system
                            </div>
                        </div>

                        {/* Shared Workspace */}
                        <div className="bg-card rounded-lg border p-6">
                            <div className="flex items-center mb-4">
                                <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center mr-4">
                                    <span className="text-2xl">🏢</span>
                                </div>
                                <div>
                                    <h3 className="text-xl font-semibold">Shared Workspace</h3>
                                    <p className="text-muted-foreground">Collaborative project management</p>
                                </div>
                            </div>
                            <p className="text-muted-foreground mb-4">
                                Organize projects, share files, and track progress in dedicated workspaces for teams.
                            </p>
                            <div className="bg-muted rounded p-3 text-sm text-muted-foreground">
                                Coming soon: Project management tools
                            </div>
                        </div>
                    </div>

                    <div className="mt-12">
                        <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-8 text-center">
                            <h2 className="text-2xl font-semibold mb-4">🔨 Under Construction</h2>
                            <p className="text-muted-foreground mb-6">
                                We are building amazing collaboration tools that will transform how teams work together. 
                                Stay tuned for updates!
                            </p>
                            <div className="flex justify-center space-x-4 text-sm">
                                <span className="bg-background px-3 py-1 rounded-full">Real-time Sync</span>
                                <span className="bg-background px-3 py-1 rounded-full">Multi-platform</span>
                                <span className="bg-background px-3 py-1 rounded-full">Secure</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}