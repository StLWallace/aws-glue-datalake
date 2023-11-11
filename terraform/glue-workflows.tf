resource "aws_glue_workflow" "ticketmaster" {
  name = "ticketmaster-${var.environment}"
}

resource "aws_glue_trigger" "start" {
  name          = "ticketmast-start-${var.environment}"
  type          = "ON_DEMAND"
  workflow_name = aws_glue_workflow.ticketmaster.name

  actions {
    job_name = aws_glue_job.venues_raw.name
  }

  actions {
    job_name = aws_glue_job.events_raw.name
  }
}

resource "aws_glue_trigger" "venues_processed" {
  name          = "venues-processed-${var.environment}"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.ticketmaster.name

  predicate {
    conditions {
      job_name = aws_glue_job.venues_raw.name
      state    = "SUCCEEDED"
    }
  }

  actions {
    job_name = aws_glue_job.venues_processed.name
  }
}

resource "aws_glue_trigger" "events_processed" {
  name          = "events-processed-${var.environment}"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.ticketmaster.name

  predicate {
    conditions {
      job_name = aws_glue_job.events_raw.name
      state    = "SUCCEEDED"
    }
  }

  actions {
    job_name = aws_glue_job.events_processed.name
  }
}

resource "aws_glue_trigger" "crawler" {
  name          = "tickemaster-crawler-${var.environment}"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.ticketmaster.name

  predicate {
    conditions {
      job_name = aws_glue_job.events_processed.name
      state    = "SUCCEEDED"
    }

    conditions {
      job_name = aws_glue_job.venues_processed.name
      state    = "SUCCEEDED"
    }
  }

  actions {
    crawler_name = aws_glue_crawler.ticketmaster.name
  }
}
