import { getTranslations } from 'next-intl/server';
import { Metadata } from 'next';
import { PageHeader } from '@/shared/ui/page-header';
import { Box } from '@/shared/ui/box';
import { HubIcon, MessageIcon, QuestionIcon, BookIcon, PaletteIcon, ConstructionIcon } from '@/shared/ui/icons';

export async function generateMetadata(): Promise<Metadata> {
    const t = await getTranslations('navigation');

    return {
        title: `${t('hub')} - Community Forum`,
        description: 'Community forum for user-generated content and discussions',
    };
}

export default async function HubPage() {
    const t = await getTranslations('navigation');

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-6xl mx-auto">
                    <PageHeader
                        icon={<HubIcon size={24} />}
                        iconClassName="bg-orange-500/15 text-orange-600 dark:bg-orange-500/20 dark:text-orange-400"
                        title={t('hub')}
                        description="Community forum for user-generated content, discussions, and knowledge sharing."
                    />

                    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                        {/* Forum Categories */}
                        <div className="lg:col-span-3">
                            <h2 className="text-2xl font-semibold mb-6">Forum Categories</h2>

                            <div className="space-y-4">
                                {/* General Discussion */}
                                <Box size="lg">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-4">
                                            <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
                                                <MessageIcon size={24} />
                                            </div>
                                            <div>
                                                <h3 className="text-xl font-semibold">General Discussion</h3>
                                                <p className="text-muted-foreground">Open conversations about any topic</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-sm font-medium">1,234 posts</div>
                                            <div className="text-xs text-muted-foreground">Last: 2h ago</div>
                                        </div>
                                    </div>
                                </Box>

                                {/* Q&A */}
                                <Box size="lg">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-4">
                                            <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
                                                <QuestionIcon size={24} />
                                            </div>
                                            <div>
                                                <h3 className="text-xl font-semibold">Questions & Answers</h3>
                                                <p className="text-muted-foreground">Get help from the community</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-sm font-medium">856 posts</div>
                                            <div className="text-xs text-muted-foreground">Last: 1h ago</div>
                                        </div>
                                    </div>
                                </Box>

                                {/* Tutorials */}
                                <Box size="lg">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-4">
                                            <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center">
                                                <BookIcon size={24} />
                                            </div>
                                            <div>
                                                <h3 className="text-xl font-semibold">Tutorials & Guides</h3>
                                                <p className="text-muted-foreground">Share knowledge and learn new skills</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-sm font-medium">432 posts</div>
                                            <div className="text-xs text-muted-foreground">Last: 3h ago</div>
                                        </div>
                                    </div>
                                </Box>

                                {/* Showcase */}
                                <Box size="lg">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-4">
                                            <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center">
                                                <PaletteIcon size={24} />
                                            </div>
                                            <div>
                                                <h3 className="text-xl font-semibold">Showcase</h3>
                                                <p className="text-muted-foreground">Show off your projects and creations</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-sm font-medium">298 posts</div>
                                            <div className="text-xs text-muted-foreground">Last: 5h ago</div>
                                        </div>
                                    </div>
                                </Box>
                            </div>
                        </div>

                        {/* Sidebar */}
                        <div className="lg:col-span-1">
                            <div className="space-y-6">
                                {/* Community Stats */}
                                <Box size="lg">
                                    <h3 className="font-semibold mb-4">Community Stats</h3>
                                    <div className="space-y-3">
                                        <div className="flex justify-between">
                                            <span className="text-muted-foreground">Members</span>
                                            <span className="font-medium">15,234</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-muted-foreground">Topics</span>
                                            <span className="font-medium">2,820</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-muted-foreground">Posts</span>
                                            <span className="font-medium">28,567</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-muted-foreground">Online</span>
                                            <span className="font-medium text-green-600">234</span>
                                        </div>
                                    </div>
                                </Box>

                                {/* Recent Activity */}
                                <Box size="lg">
                                    <h3 className="font-semibold mb-4">Recent Activity</h3>
                                    <div className="space-y-3 text-sm">
                                        <div className="text-muted-foreground">
                                            <span className="font-medium">User123</span> posted in General Discussion
                                        </div>
                                        <div className="text-muted-foreground">
                                            <span className="font-medium">DevPro</span> answered a question
                                        </div>
                                        <div className="text-muted-foreground">
                                            <span className="font-medium">Designer</span> shared a new tutorial
                                        </div>
                                    </div>
                                </Box>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
