import type { Metadata } from "next";
import { AppRouterCacheProvider } from "@mui/material-nextjs/v15-appRouter";
import { CssBaseline } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";
import Content from "@/components/layout/Content";
import Children from "@/components/layout/Children";
import Footer from "@/components/layout/Footer";
import Header from "@/components/layout/Header";
import theme from '@/theme';

export const metadata: Metadata = {
  title: "Endobelle",
  description: "Jestem tu, jeśli mnie potrzebujesz",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AppRouterCacheProvider>
          <ThemeProvider theme={theme}>
            <Content>
              <CssBaseline />
              <Header />
              <Children>
                { children }
              </Children>
              <Footer />
            </Content>
          </ThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}

