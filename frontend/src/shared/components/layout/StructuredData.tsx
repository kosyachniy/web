export default function StructuredData() {
    const structuredData = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "web",
        "description": "Template web app",
        "url": "https://web.chill.services",
        "logo": "https://web.chill.services/logo.svg",
        "sameAs": [
            "https://web.chill.services"
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "Customer Service",
            "availableLanguage": ["English", "Russian", "Chinese", "Spanish", "Arabic"]
        },
        "foundingDate": "2024",
        "knowsAbout": [
            "Web Development",
            "Full Stack Development",
            "Digital Solutions"
        ],
        "makesOffer": {
            "@type": "Offer",
            "itemOffered": {
                "@type": "Service",
                "name": "web",
                "description": "Template web app"
            }
        }
    };

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{
                __html: JSON.stringify(structuredData),
            }}
        />
    );
}
