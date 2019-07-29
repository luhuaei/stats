## map function base dict.
map <- function(df, dict){
    res <- list()
    for (m in colnames(df)){
        if (m %in% names(dict)){
            d <- df[[m]]
            s <- dict[[m]]
            res[[m]] <- sapply(d, function(x){
                s[as.character(x)]
            })
        }
    }
    res
}
