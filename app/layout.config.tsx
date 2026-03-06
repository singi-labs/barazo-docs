import Image from 'next/image'
import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared'

export const baseOptions: BaseLayoutProps = {
  nav: {
    title: (
      <>
        <Image
          src="/barazo-logo-light.svg"
          alt="Barazo"
          width={28}
          height={28}
          className="dark:hidden"
        />
        <Image
          src="/barazo-logo-dark.svg"
          alt="Barazo"
          width={28}
          height={28}
          className="hidden dark:block"
        />
        <span className="font-semibold">Barazo Docs</span>
      </>
    ),
  },
  githubUrl: 'https://github.com/singi-labs',
  links: [
    {
      text: 'Forum',
      url: 'https://barazo.forum',
    },
  ],
}
