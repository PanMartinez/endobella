import Container from "@mui/material/Container"
import Copyright from '@/components/Copyright';

export default function Footer() {
  return (
    <Container
      component="footer"
      maxWidth={false}
      sx={{
        flex: 1,
        backgroundColor: 'background.paper',
        py: 3,
        mt: 'auto',
      }}>
      <Copyright/>
    </Container>
  )
}
