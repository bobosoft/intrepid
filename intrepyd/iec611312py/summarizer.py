"""
Copyright (C) 2018 Roberto Bruttomesso <roberto.bruttomesso@gmail.com>

This file is distributed under the terms of the 3-clause BSD License.
A copy of the license can be found in the root directory or at
https://opensource.org/licenses/BSD-3-Clause.

Author: Roberto Bruttomesso <roberto.bruttomesso@gmail.com>
  Date: 27/12/2018

This module implements a summarizer for ST assignments
"""

from intrepyd.iec611312py.expression import Expression, VariableOcc, ConstantOcc, Ite
from intrepyd.iec611312py.statement import Assignment
from collections import OrderedDict

indent = 0
def begin(text):
    global indent
    print indent * ' ' + text + ' BEGIN'
    indent += 2

def end(text):
    global indent
    print indent * ' ' + text + ' END'
    indent -= 2

def summarizeStmtBlock(block):
    summary = OrderedDict()
    for assignment in block:
        if not isinstance(assignment, Assignment):
            raise RuntimeError('A non-assignment instruction was detected ' + str(type(assignment)))
        newRhs = substitute(assignment.rhs, summary)
        print 'Summarized %d / %d' % (len(summary) + 1, len(block))
        summary[assignment.lhs.var] = newRhs
    return [Assignment(VariableOcc(lhs), rhs) for lhs, rhs in summary.iteritems()]

def substituteInTerm(var, expression, term):
    result = None
    if isinstance(term, Expression):
        new_arguments = []
        for argument in term.arguments:
            new_arguments.append(substituteInTerm(var, expression, argument))
        result = Expression(term.operator, new_arguments)
    elif isinstance(term, Ite):
        i = substituteInTerm(var, expression, term.condition)
        t = substituteInTerm(var, expression, term.then_term)
        e = substituteInTerm(var, expression, term.else_term)
        result = Ite(i, t, e)
    elif isinstance(term, ConstantOcc):
        result = term
    elif isinstance(term, VariableOcc):
        if var == term.var:
            result = expression
        result = term
    else:
        raise NotImplementedError('Term not handled %s' % type(term))
    return result

def substitute(rhs, summary):
    result = rhs
    for key, value in summary.iteritems():
        result = substituteInTerm(key, value, result)
    return result