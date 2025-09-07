import { Container } from "@mui/material"
import Copyright from '@/components/Copyright';

export default function Footer() {
  return (
    <Container
      maxWidth={false}
      sx={{
        flex: 1,
        backgroundColor: 'background.paper',
        py: 3,
      }}>
      <Copyright/>
    </Container>
  )
}