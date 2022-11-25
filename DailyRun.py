from DailyReport import DailyReport


def runDailyReport():
    d = DailyReport()
    print(d)
    x = d.updateBlog()
    print(x)

def run():
    runDailyReport()

run()