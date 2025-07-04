import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter';
import { Roboto } from 'next/font/google';
import { ThemeProvider } from '@mui/material/styles';
import theme from '../theme';
import "./globals.css";

export const metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

const roboto = Roboto({
  weight: ['300', '400', '500', '700'],
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={roboto.variable}>
      <body>
        <AppRouterCacheProvider>
          <ThemeProvider theme={theme}>
          {children}
          </ThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
