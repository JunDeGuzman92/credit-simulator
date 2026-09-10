# Credit Score Simulator - Frontend

Next.js 14 frontend application for the Credit Score Simulator. Built with React 18, TypeScript, Tailwind CSS, and shadcn/ui components.

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### Build

```bash
npm run build
npm start
```

## Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── app/                    # App Router pages
│   ├── page.tsx           # Main landing page
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/             # Reusable UI components
├── lib/                   # Utility functions
├── public/                # Static assets
├── next.config.ts         # Next.js configuration
├── tailwind.config.ts     # Tailwind CSS configuration
└── tsconfig.json          # TypeScript configuration
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000` by default. Configure via `NEXT_PUBLIC_API_URL` environment variable.

## Styling

- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Accessible component primitives
- **Lucide Icons**: Icon library

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)

## Deployment

Deploy to Vercel with zero configuration:

```bash
npx vercel
```

Or connect your GitHub repository to Vercel for automatic deployments.