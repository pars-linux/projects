#!/usr/bin/python
# -*- coding: utf-8 -*-

class generator():
    '''
    This Class takes a dictionary specialized for Pardus tests and produce an html report page
    '''

    def __init__(self,testDict):
        self.testDict = testDict

    def generate(self):
        report = ["<table align=center border=2>\n \
                    <caption>Rapor</caption>\n \
                    <tbody align=center>\n \
                    <tr>\n \
                        <td>Package Name</td>\n \
                        <td>Status</td>\n \
                        <td>Comment</td>\n \
                    </tr>\n"]
        append = report.append
        for package in self.testDict:
            if self.testDict[package].status:
                append('<tr BGCOLOR="#00FF00"> <td>%s</td>\n' % self.testDict[package].packageName)
            else:
                append('<tr BGCOLOR="#FF0000" ><td>%s</td>\n' % self.testDict[package].packageName)
            append("<td>%s</td>\n" % self.testDict[package].status)
            append("<td>%s</td></tr>\n" % self.testDict[package].comment)
        append("</tbody></table>\n")
        reportString = "\n ".join(report)
        return reportString
