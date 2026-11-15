# Extractable components

## AppHeader
- Source: `web/src/App.tsx` (header.top + p.strip)
- Category: layout
- Description: Title, mission strip ("Mars transit", day), large day clock with hour, Play/Continue/Replay button
- Extractable props: day (number), playing (boolean)
- Hardcoded: title text, strip text, CSS

## CrewCard
- Source: `web/src/components/CrewList.tsx`
- Category: basic
- Description: Selected crew member card with segmented body figure, name and one-line status
- Extractable props: state (expected | event | unexplained | crew)
- Hardcoded: figure artwork, CSS

## CrewRow
- Source: `web/src/components/CrewList.tsx`
- Category: basic
- Description: One-line crew row: status mark, name, status text
- Extractable props: state, selected (boolean)

## AlertCard
- Source: `web/src/components/AlertPanel.tsx`
- Category: basic
- Description: Astronaut card with OBSERVATION / CHECK NOW / ESCALATE IF, "Not a diagnosis.", collapsible numbers and handover note
- Extractable props: none that vary per page

## MonitorLane
- Source: `web/src/components/Figure.tsx`
- Category: basic
- Description: One monitor row under the chart: name, how it works, alert ticks on the day axis, false-alarm count
- Extractable props: highlighted (boolean)
