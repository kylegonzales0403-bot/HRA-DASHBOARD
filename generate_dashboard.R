# ============================================================
# Generate HR Dashboard as index.html (GitHub Pages ready)
# ============================================================

# Install packages if needed
packages <- c("rmarkdown", "flexdashboard", "plotly", "DT", "tidyverse")
new_pkgs <- packages[!(packages %in% installed.packages()[,"Package"])]
if(length(new_pkgs)) {
  cat("Installing required packages...\n")
  install.packages(new_pkgs, repos = "https://cloud.r-project.org/")
}

# Load libraries
library(rmarkdown)
library(flexdashboard)
library(plotly)
library(DT)
library(tidyverse)

# R Markdown content (your HR metrics)
rmd_content <- '---
title: "HR Metrics Dashboard"
output: 
  flexdashboard::flex_dashboard:
    orientation: rows
    vertical_layout: fill
    theme: cosmo
    self_contained: true
---

```{r setup, include=FALSE}
library(flexdashboard)
library(plotly)
library(DT)
library(tidyverse)

overall_df <- data.frame(
  Site = c("Sec 1", "Sec 2", "Sec 3", "Sec 4"),
  Absenteeism_Rate = c(0.0645, 0.0208, 0.0, 0.0),
  Tardiness_Rate   = c(0.0045, 0.0033, 0.0012, 0.0050),
  Undertime_Rate   = c(0.0000, 0.0002, 0.0000, 0.0000),
  Turnover_Rate    = c(0.3355, 0.2727, 0.2500, 0.0000),
  Retention_Rate   = c(0.6667, 0.7222, 0.7500, 1.0000),
  FlightRisk_Rate  = c(0.3396, 0.2674, 0.2500, 0.0000)
)

overtime_df <- data.frame(
  Site = c("Sec 1", "Sec 2", "Sec 3", "Sec 4"),
  Overtime_Rate = c(0.2816, 0.0822, 0.1502, 0.0031)
)

hr_df <- overall_df %>%
  left_join(overtime_df, by = "Site") %>%
  mutate(across(where(is.numeric), ~ round(.x, 4)))

create_bar <- function(df, metric, color, title) {
  df %>%
    plot_ly(x = ~Site, y = ~get(metric), type = "bar",
            marker = list(color = color),
            text = ~paste(scales::percent(get(metric), accuracy = 0.01)),
            textposition = "outside",
            hoverinfo = "text",
            hovertemplate = paste("%{x}<br>Rate: %{text}<extra></extra>")) %>%
    layout(yaxis = list(title = "Rate", tickformat = ".0%"),
           xaxis = list(title = ""),
           title = list(text = title, font = list(size = 12)))
}
```

## Dashboard {data-orientation="rows"}

### Row 1

#### Absenteeism Rate
```{r}
create_bar(hr_df, "Absenteeism_Rate", "#1f77b4", "Absenteeism Rate by Site")
```

#### Tardiness Rate
```{r}
create_bar(hr_df, "Tardiness_Rate", "#ff7f0e", "Tardiness Rate by Site")
```

#### Undertime Rate
```{r}
create_bar(hr_df, "Undertime_Rate", "#2ca02c", "Undertime Rate by Site")
```

### Row 2

#### Turnover Rate
```{r}
create_bar(hr_df, "Turnover_Rate", "#d62728", "Turnover Rate by Site")
```

#### Retention Rate
```{r}
create_bar(hr_df, "Retention_Rate", "#9467bd", "Retention Rate by Site")
```

#### Flight Risk Rate
```{r}
create_bar(hr_df, "FlightRisk_Rate", "#8c564b", "Flight Risk Rate by Site")
```

### Row 3

#### Overtime Rate
```{r}
create_bar(hr_df, "Overtime_Rate", "#e377c2", "Overtime Rate by Site")
```

### Row 4 {data-height=400}

#### Summary Table
```{r}
datatable(hr_df, 
          options = list(pageLength = 5, dom = "tp"),
          rownames = FALSE,
          caption = "HR Metrics Summary by Site") %>%
  formatPercentage(columns = c(2:7), digits = 2)
```

'

# Write the R Markdown file
cat("Creating R Markdown file...\n")
writeLines(rmd_content, "dashboard.Rmd")

# Render to HTML
cat("Rendering dashboard to HTML...\n")
rmarkdown::render("dashboard.Rmd", 
                  output_file = "index.html",
                  output_format = "flexdashboard::flex_dashboard",
                  quiet = FALSE)

cat("\n✓ Dashboard successfully generated!\n")
cat("✓ Output file: index.html\n")
cat("✓ Ready for GitHub Pages deployment!\n")
