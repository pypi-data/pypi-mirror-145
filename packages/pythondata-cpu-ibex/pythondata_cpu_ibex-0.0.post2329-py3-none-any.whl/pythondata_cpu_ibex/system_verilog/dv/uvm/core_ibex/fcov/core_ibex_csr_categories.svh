// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

// List of CSRs to ignore for coverage purposes. These CSRs are ignored as they
// are less critical and achieving full coverage isn't necessary.
`define IGNORED_CSRS \
  // Performance counter control \
  CSR_MCOUNTINHIBIT, \
  CSR_MCOUNTEREN, \
  CSR_MHPMEVENT3, \
  CSR_MHPMEVENT4, \
  CSR_MHPMEVENT5, \
  CSR_MHPMEVENT6, \
  CSR_MHPMEVENT7, \
  CSR_MHPMEVENT8, \
  CSR_MHPMEVENT9, \
  CSR_MHPMEVENT10, \
  CSR_MHPMEVENT11, \
  CSR_MHPMEVENT12, \
  CSR_MHPMEVENT13, \
  CSR_MHPMEVENT14, \
  CSR_MHPMEVENT15, \
  CSR_MHPMEVENT16, \
  CSR_MHPMEVENT17, \
  CSR_MHPMEVENT18, \
  CSR_MHPMEVENT19, \
  CSR_MHPMEVENT20, \
  CSR_MHPMEVENT21, \
  CSR_MHPMEVENT22, \
  CSR_MHPMEVENT23, \
  CSR_MHPMEVENT24, \
  CSR_MHPMEVENT25, \
  CSR_MHPMEVENT26, \
  CSR_MHPMEVENT27, \
  CSR_MHPMEVENT28, \
  CSR_MHPMEVENT29, \
  CSR_MHPMEVENT30, \
  CSR_MHPMEVENT31, \
  // Performance counters \
  CSR_MCYCLE, \
  CSR_MINSTRET, \
  CSR_MHPMCOUNTER3, \
  CSR_MHPMCOUNTER4, \
  CSR_MHPMCOUNTER5, \
  CSR_MHPMCOUNTER6, \
  CSR_MHPMCOUNTER7, \
  CSR_MHPMCOUNTER8, \
  CSR_MHPMCOUNTER9, \
  CSR_MHPMCOUNTER10, \
  CSR_MHPMCOUNTER11, \
  CSR_MHPMCOUNTER12, \
  CSR_MHPMCOUNTER13, \
  CSR_MHPMCOUNTER14, \
  CSR_MHPMCOUNTER15, \
  CSR_MHPMCOUNTER16, \
  CSR_MHPMCOUNTER17, \
  CSR_MHPMCOUNTER18, \
  CSR_MHPMCOUNTER19, \
  CSR_MHPMCOUNTER20, \
  CSR_MHPMCOUNTER21, \
  CSR_MHPMCOUNTER22, \
  CSR_MHPMCOUNTER23, \
  CSR_MHPMCOUNTER24, \
  CSR_MHPMCOUNTER25, \
  CSR_MHPMCOUNTER26, \
  CSR_MHPMCOUNTER27, \
  CSR_MHPMCOUNTER28, \
  CSR_MHPMCOUNTER29, \
  CSR_MHPMCOUNTER30, \
  CSR_MHPMCOUNTER31, \
  CSR_MCYCLEH, \
  CSR_MINSTRETH, \
  CSR_MHPMCOUNTER3H, \
  CSR_MHPMCOUNTER4H, \
  CSR_MHPMCOUNTER5H, \
  CSR_MHPMCOUNTER6H, \
  CSR_MHPMCOUNTER7H, \
  CSR_MHPMCOUNTER8H, \
  CSR_MHPMCOUNTER9H, \
  CSR_MHPMCOUNTER10H, \
  CSR_MHPMCOUNTER11H, \
  CSR_MHPMCOUNTER12H, \
  CSR_MHPMCOUNTER13H, \
  CSR_MHPMCOUNTER14H, \
  CSR_MHPMCOUNTER15H, \
  CSR_MHPMCOUNTER16H, \
  CSR_MHPMCOUNTER17H, \
  CSR_MHPMCOUNTER18H, \
  CSR_MHPMCOUNTER19H, \
  CSR_MHPMCOUNTER20H, \
  CSR_MHPMCOUNTER21H, \
  CSR_MHPMCOUNTER22H, \
  CSR_MHPMCOUNTER23H, \
  CSR_MHPMCOUNTER24H, \
  CSR_MHPMCOUNTER25H, \
  CSR_MHPMCOUNTER26H, \
  CSR_MHPMCOUNTER27H, \
  CSR_MHPMCOUNTER28H, \
  CSR_MHPMCOUNTER29H, \
  CSR_MHPMCOUNTER30H, \
  CSR_MHPMCOUNTER31H, \
  // Must exist when implementing hardware triggers (breakpoints), but read as 0 and ignore \
  // writes. Unused/Uneeded by debugger infrastructure. \
  // TODO: Don't ignore these? \
  CSR_MCONTEXT, \
  CSR_SCONTEXT

// Debug related CSRs
`define DEBUG_CSRS \
  CSR_DCSR, \
  CSR_DPC, \
  CSR_DSCRATCH0, \
  CSR_DSCRATCH1, \
  CSR_TSELECT, \
  CSR_TDATA1, \
  CSR_TDATA2, \
  CSR_TDATA3

