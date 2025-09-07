'use client'
import { createTheme } from '@mui/material/styles';
import { Mulish } from 'next/font/google'

const font = Mulish({
  weight: ['300'],
  subsets: ['latin'],
  display: 'swap',
})

const theme = createTheme(
  {
    colorSchemes:
      {
        light:
          {
            palette: {
              primary: {
                main: '#000000',
              },
              secondary: {
                main: '#ffffff',
              },
              background: {
                default: '#ffffff',
                paper: '#fcf4f4',
              },
              text: {
                primary: '#000000',
                secondary: '#333333',
              },
            }
          },

        dark:
          {
            palette: {
              primary: {
                main: '#ffffff',
              },
              secondary: {
                main: '#000000',
              },
              background: {
                default: '#121212',
                paper: '#412828',
              },
              text: {
                primary: '#ffffff',
                secondary: '#cccccc',
              },
            },
          },
      },
        typography: {
      fontFamily: font.style.fontFamily,
    },
  },
)

export default theme