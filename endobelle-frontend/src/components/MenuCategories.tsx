import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";

export default function MenuCategories() {
  return (
    <Grid container spacing={2} sx={{ flexGrow: 1 }}>
      <Grid size={4} display={'flex'} justifyContent={'flex-start'} alignItems={'center'}>
        <Typography color="primary">
          Blog
        </Typography>
      </Grid>
      <Grid size={4} display={'flex'} justifyContent={'flex-start'} alignItems={'center'}>
        <Typography color="primary">
          Sklep
        </Typography>
      </Grid>
      <Grid size={4} display={'flex'} justifyContent={'flex-start'} alignItems={'center'}>
        <Typography color="primary">
          O nas
        </Typography>
      </Grid>
    </Grid>
  )
}
