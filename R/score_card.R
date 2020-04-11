woe_iv <- function(x, y){
    "计算x与y的woe值与iv值。x为变量，y为标签。返回列表"
    if (length(x) != length(y)) stop("The length different of x and y.")
    d <- data.frame(x = x, y = y)
    xbins <- sort(unique(x))
    woes <- xbins
    names(woes) <- as.character(xbins)
    ivs <- woes

    bt <- nrow(subset(d, y == 1))
    gt <- nrow(subset(d, y == 0))
    for (xbin in xbins){
        dset <- d[d$x == xbin, ]
        bi <- nrow(subset(dset, y == 1))
        gi <- nrow(subset(dset, y == 0))
        pbi <- bi / bt
        pgi <- gi / gt
        w <- log(pbi / pgi)
        ## 存在一些计算得到无穷的情况，将替换成0
        if (is.infinite(w)) w <- 0
        woes[as.character(xbin)] <- w
        iv <- (pbi - pgi) * w
        ivs[as.character(xbin)] <- iv
    }
    list(woe = woes, iv = ivs)
}


woe_exchange <- function(d, y){
    "对分类变量进行woe转变。返回列表"
    lapply(d, function(s) {
        woe <- woe_iv(s, y)$woe
        sapply(s, function(x) woe[as.character(x)])
    })
}


score <- function(df, B, fit){
    "计算每一个变量的得分。
df为数据集，B为常数，fit为模型对象。返回评分表(list)"
    res <- list()
    coefs <- fit$coefficients
    m <- intersect(names(coefs), colnames(df))
    for (name in m){
        d <- df[[name]]
        coef <- coefs[name]
        b <- sort(unique(d))
        s <- round(B * b * coef)
        names(s) <- as.character(1:length(b))
        res[[name]] <- s
    }
    res
}


map <- function(df, dict){
    "映射函数。
根据dict中的变量将df中的数据进行替换。"
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


total_score <- function(df, A, st){
    "计算每一个样本的总得分。
df 为数据集，A为基础分，st为评分表，返回数据框结构。"
    d <- as.data.frame(map(df, st))
    total <- apply(d, 1, function(x) sum(x, na.rm = TRUE))
    d[["total"]] <- A + total
    d
}
