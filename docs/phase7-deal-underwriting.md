# PHASE 7 — DEAL UNDERWRITING ENGINE

## Goal

Establish the initial autonomous deal underwriting foundation for the AI Real Estate Deal Intelligence Machine.

## Scope

This phase introduces a bounded underwriting decision layer capable of supporting:

- WHOLESALE
- FIX AND FLIP
- BUY AND HOLD
- BRRRR
- CREATIVE FINANCE

## Inputs Evaluated

- purchase price
- ARV
- repairs
- closing costs
- holding costs
- financing
- selling costs
- desired profit
- assignment fee
- cash flow

## Outputs

- Maximum Offer
- Offer Range
- Estimated Profit
- ROI
- Cash-on-Cash Return
- Cap Rate
- Assignment Spread

## Behavior

The underwriting engine will rerun when important inputs change, and it emits an underwriting event when an update is generated.

## Constraints

- No acquisition or disposition execution is added in this phase.
- The underwriting foundation is local and mock-backed.
- The result is an explainable decision support model only.
