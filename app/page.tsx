import Link from 'next/link'
import Image from 'next/image'
import { SiteFooter } from '@/components/site-footer'

const audiences = [
  {
    title: 'Using Barazo',
    description:
      'Get started as a forum member. Sign in with your AT Protocol account, post your first topic, and learn what each feature does.',
    href: '/docs/using',
  },
  {
    title: 'Administration',
    description:
      'Run and moderate a forum. Categories, moderation, branding, and content maturity, plus self-hosting and managed hosting.',
    href: '/docs/administration',
  },
  {
    title: 'Developer',
    description:
      'Build on the Barazo platform. Lexicon schemas, API reference, plugin development, and AT Protocol integration.',
    href: '/docs/developer',
  },
]

export default function HomePage() {
  return (
    <>
      <main className="flex min-h-screen flex-col items-center px-4 py-16">
        <div className="flex flex-col items-center gap-4 text-center">
          <Image
            src="/barazo-logo-light.svg"
            alt="Barazo"
            width={64}
            height={64}
            className="dark:hidden"
          />
          <Image
            src="/barazo-logo-dark.svg"
            alt="Barazo"
            width={64}
            height={64}
            className="hidden dark:block"
          />
          <h1 className="text-3xl font-bold tracking-tight">Barazo Docs</h1>
          <p className="max-w-lg text-fd-muted-foreground">
            Documentation for the federated forum platform built on the AT Protocol.
          </p>
        </div>

        <div className="mt-12 grid w-full max-w-4xl gap-4 sm:grid-cols-3">
          {audiences.map((audience) => (
            <Link
              key={audience.href}
              href={audience.href}
              className="group rounded-lg border border-fd-border p-6 transition-colors hover:border-fd-primary hover:bg-fd-accent/50"
            >
              <h2 className="mb-2 text-lg font-semibold group-hover:text-fd-primary">
                {audience.title}
              </h2>
              <p className="text-sm text-fd-muted-foreground">{audience.description}</p>
            </Link>
          ))}
        </div>
      </main>
      <SiteFooter />
    </>
  )
}
