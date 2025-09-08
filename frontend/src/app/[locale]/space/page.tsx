import { getTranslations } from 'next-intl/server';
import { Metadata } from 'next';
import { PageHeader } from '@/shared/ui/page-header';
import { Box } from '@/shared/ui/box';
import { SpaceIcon, WhiteboardIcon, VideoIcon, MessageIcon, BuildingIcon, ConstructionIcon } from '@/shared/ui/icons';

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
                        <Box size="lg">
                            <div className="flex items-center mb-4">
                                <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
                                    <WhiteboardIcon size={24} />
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
                        </Box>

                        {/* Video Chat */}
                        <Box size="lg">
                            <div className="flex items-center mb-4">
                                <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mr-4">
                                    <VideoIcon size={24} />
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
                        </Box>

                        {/* Messenger */}
                        <Box size="lg">
                            <div className="flex items-center mb-4">
                                <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mr-4">
                                    <MessageIcon size={24} />
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
                        </Box>

                        {/* Shared Workspace */}
                        <Box size="lg">
                            <div className="flex items-center mb-4">
                                <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center mr-4">
                                    <BuildingIcon size={24} />
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
                        </Box>
                    </div>
                </div>
            </div>
        </div>
    );
}
