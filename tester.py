import cross_validator as cv

if __name__=="__main__":
    cross_validator = cv.cross_validator(5,"/features",200)
    cross_validator.k_fold_cross_validation()