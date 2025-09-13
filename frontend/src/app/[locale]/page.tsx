'use client';

import { CounterDemo, UserDemo, PopupDemo, ToastDemo, MultiFileUploadDemo } from '@/features/demo';
import { ThreeColumnLayout } from '@/widgets/three-column-layout';
import { SectionsSidebar } from '@/widgets/sections-sidebar';
import { FastActionsSidebar } from '@/widgets/fast-actions-sidebar';
import { ContactFormSidebar } from '@/widgets/contact-form-sidebar';
import { QuestionnaireSidebar } from '@/widgets/questionnaire-sidebar';
import { PageHeader } from '@/shared/ui/page-header';
import { Card } from '@/shared/ui/card';
import { PostsIcon, TagIcon, CalendarIcon } from '@/shared/ui/icons';

export default function Home() {
    const leftSidebar = (
        <>
            <SectionsSidebar />
        </>
    );

    const rightSidebar = (
        <>
            <FastActionsSidebar />
            <ContactFormSidebar />
            <QuestionnaireSidebar />
        </>
    );

    const mockPosts = [
        { id: 1, title: "Introduction to React 19", category: "Technology", date: "2 days ago" },
        { id: 2, title: "Machine Learning Basics", category: "Science", date: "1 week ago" },
        { id: 3, title: "Business Strategies 2024", category: "Business", date: "3 days ago" },
        { id: 4, title: "Design Systems Guide", category: "Design", date: "5 days ago" },
        { id: 5, title: "Web Performance Tips", category: "Technology", date: "1 day ago" },
        { id: 6, title: "Data Analysis Methods", category: "Science", date: "4 days ago" }
    ];

    return (
        <ThreeColumnLayout 
            leftSidebar={leftSidebar} 
            rightSidebar={rightSidebar}
            rightSidebarSticky={false}
        >
            <div className="space-y-12">
                {/* Demo Components */}
                <div className="space-y-8">
                    <div className="max-w-2xl mx-auto space-y-8">
                        <CounterDemo />
                        <UserDemo />
                        <PopupDemo />
                        <ToastDemo />
                    </div>
                    <MultiFileUploadDemo />
                </div>

                {/* Posts Section */}
                <div className="space-y-6">
                    <PageHeader
                        icon={<PostsIcon size={24} />}
                        iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400"
                        title="Posts (3-Column Demo)"
                        description="Example of how the posts page would look with sidebar blocks"
                    />

                    {/* Mock Posts Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {mockPosts.map((post) => (
                            <Card 
                                key={post.id}
                                title={post.title}
                                description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt..."
                                images={[]}
                                filters={[
                                    {
                                        icon: <TagIcon size={12} />,
                                        value: post.category
                                    },
                                    {
                                        icon: <CalendarIcon size={12} />,
                                        value: post.date
                                    }
                                ]}
                                variant="default"
                                onClick={() => {
                                    console.log('Post clicked:', post.title);
                                }}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </ThreeColumnLayout>
    );
}
