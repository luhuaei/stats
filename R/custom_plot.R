## Add time label to time series plot.
plot_ts <- function(data, years, months){
    gendate <- function(years, months){
        results <- c()
        for (y in years[1]:years[2]){
            for (m in months[1]:months[2]){
                results <- append(results, paste(y, m, sep = "-"))
            }
        }
        results
    }

    n <- length(data)
    index <- 1:n
    y <- years[2] - years[1] + 1
    date <- gendate(years, months)
    ix <- seq(1, n, length.out = length(date))
    plot(data, xaxt = "n", type = "l", xlab = "")
    axis(side = 1, at = index[ix], labels = date, las = 2)
}
plot_ts(rnorm(1000), c(2018, 2019), c(6, 12))
