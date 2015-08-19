# BremertonRoundTrip

This is the repository for an informal hack project launched Aug 20-22 during the LSST collaboration meeting in Bremerton, WA.

The goal of this project is try and assemble a "round-trip" weak-lensing reference analysis that is suitable for
studying the impact of pixel-level systematics on cosmology.  The flow chart below shows the basic round-trip structure. Dashed blue lines show short cuts that provide intermediate comparison points and allow higher- and lower-level paths to be developed and tested independently.

Although our goals sound ambitious, the idea is to ruthlessly simplify each component and aim for a chain that is
complete rather than of high fidelity. A lot of detailed work is already in progress on pieces of this, so the
goal here is to "see the whole elephant" rather than work on an ear or a tusk.

Many of necessary pieces already exist so much of the work will involve selecting suitable code or algorithms from
the literature and figuring out how to connect them together.  The results will hopefully have some pedagogical value,
at least, and the process should help reveal where more effort is most needed to get scientifically useful results.

![round-trip flowchart]
(https://github.com/DarkEnergyScienceCollaboration/BremertonRoundTrip/blob/master/images/Ladder.png?raw=true)
