# HAMR SysMLv2 Microkit Library: Conversation Transcript

**Participants:** John Hatcliff (HAMR lead, K-State SAnToS lab) and HAMR Dev: Microkit SysML (a Grok Bot assistant)
**Dates:** October 25–26, 2026 (America/Chicago, CT)
**Repository:** [santoslab/hamr-sysml-microkit](https://github.com/santoslab/hamr-sysml-microkit)

This conversation covers Phase 1 of a SysMLv2 library for seL4 Microkit system description (SDF) concepts. The goal is a developer-friendly SysMLv2 representation of the seL4/Microkit configuration that sits below HAMR's AADL-style SysMLv2 architecture models. The style follows HAMR's [sysml-aadl-libraries](https://github.com/santoslab/sysml-aadl-libraries). The work ran in a Cursor cloud agent, not on John's laptop, and was delivered as a pull request.

> **Note on the text.** Messages are verbatim. Notes in _[brackets]_ mark questions with answer buttons, cards, and links to the cloud agent.

## Contents

1. [Setup](#1-setup)
2. [Phase 1 brief](#2-phase-1-brief)
3. [Repository access and launch](#3-repository-access-and-launch)
4. [Phase 1 result (PR #1)](#4-phase-1-result-pr-1)
5. [This transcript](#5-this-transcript)
6. [Outcomes](#outcomes)

---

## 1. Setup

**HAMR Dev: Microkit SysML:** Hi John! I'm ready to dig into the Microkit and SysMLv2 side of HAMR. I'll do the repo work in cloud agents under santoslab, and I can check with HAMR Infrastructure Dev whenever something overlaps with the visualizer.

To get going, can you walk me through the project? I'd mostly like to know what you're trying to build or fix first, and which santoslab repos and example models it involves.

## 2. Phase 1 brief

**John** _(Sun Oct 25, 2026, 6:04 PM CT)_**:**

As part of the development of the HAMR model-driven development tool
chain. I would like you to prototype a SysMLv2 library for
representing seL4 microkit system description file concepts. I have
created an empty repo here
(https://github.com/santoslab/hamr-sysml-microkit). 

The goal here is to support a developer-friendly representation of the
configuration of the seL4 kernel in SysMLv2. Right now, Microkit
system descriptions are low-level artifacts in either XML or Python
scripts. In the desired end state of development, a HAMR users (i.e.,
developers of microkit based seL4 systems) would be able to define
there system architectures using HAMR's existing SysMLv2 front-end.
Currently when HAMR code generation runs, it generates the low-level
XML system description file and/or Python config files. We are
considering two different options for enhancing the code-generation
pipeline architecture. In Option 1, We are interested in altering the
architecture so that this code-generation step is factored through a
SysMLv2 representation of Microkit system description concepts that
sits lower the HAMR SysMLv2 architectural models. Then that SysMLv2
microkit representation would be translated to XML or Python. The
point here is that a system developer would be able to see the
architecture of the both application structure in the existing HAMR
SysMLv2, but then would also be able to see the configuration of the
lower-level SeL4 microkit kernel configuration in a companion SysMLv2
description. Traceability information would establish the
correspondence between the higher-level AADL-based architecture
concepts and the lower-level microkit concepts. 

Users would be able to edit the microkit SysMlv2 to configure the details of virtual machines, device drivers, etc. Alternatively, in Option 2 the toolchain would produce the XML and Python directly, but still generate the SysMLv2 microkit for documentation (in this case the SysMLv2 would not be edited by the developer). In the future (not to be considered in this first round of prototyping -- you can record these in design notes), we also envision the lower-level SysMLv2 being used for

- generating graphical visualizations similar to what we are working in the HAMR Sysml Vis (https://github.com/santoslab/hamr-sysml-viz)
- supporting security analysis of the configured seL4 kernel
- supporting representation of scheduling concepts
- supporting resource analysis (memory requirements) to the configuration
- supporting libraries of configurations of seL4 and configuration of the LionsOS components that sit at a level of abstraction lower than HAMR AADL.

The inspiration and style for the SysMLv2 representation of Microkit system descriptions should be based on how AADL concepts are represented in SysMLv2 via the libraries that HAMR uses (https://github.com/santoslab/sysml-aadl-libraries). Here is the HAMR documentation (https://hamr.sireum.org/hamr-doc/sysmlv2/) for using these libraries.

The documentation for system description files can be found here https://docs.sel4.systems/projects/microkit/manual/latest/#sysdesc. I could not immediately find a schema for the microkit system description file XML or Python, but you might be able to find something in the seL4 microkit github repo (https://github.com/seL4/microkit).

Regarding phasing of the development of these new capabilities and which examples to use. The first phase of development should focus only on representing the microkit system description files that are used by HAMR systems. Here is a quick summary of the different types of output that HAMR produces for seL4.

- In simple systems without virtual machines like are used in HAMR documentation and tutorials (such as the Isolette system below), the features used are more limited. These could be addressed in a first phase, e.g., the Isolette example below or simpler examples being used in HAMR SysML Viz
- When virtual machines are included, additional Microkit system description features are used.
- HAMR generates two different versions of Microkit configurations: (1) system descriptions that utilize the seL4 domain scheduler for scheduling, (2) systems that use the MCS version of seL4. In (1) the system description file is represented in XML, in the newer option (2) system description files are represented in a new python-based specification framework. Note that the seL4 protection domain architecture for these is different (different administrative components and connections are used to represent the scheduling aspects).
  In the first phase, we will only focus on the representation of Microkit info in SysMLv2. Once the HAMR development team has reviewed the SysMLv2 representation, we will ask you to use existing HAMR infrastructure to develop an internal AST/model representation, a well-formedness checker for the representation (analogous to the HAMR SysMLv2 Type Checking), and develop the translation from the SysMLv2 microkit down to the domain scheduling representation and MCS representations.

Regarding examples, two important examples are the Isolette example and the INSPECTA Open Platform example (info given below)

Isolette HAMR example (repo location (https://github.com/loonwerks/INSPECTA-models/tree/main/isolette))

- SysMLv2 models (https://github.com/loonwerks/INSPECTA-models/tree/main/isolette/sysml)
- XML representation of the system description configure for the non-MCS, domain-scheduling version of the system (https://github.com/loonwerks/INSPECTA-models/blob/main/isolette/hamr/microkit/microkit.system)
- Python-based representation for the system description configuration for the MCS version of the generated system. (https://github.com/loonwerks/INSPECTA-models/tree/main/isolette/hamr/microkit_mcs)

INSPECTA Open Platform (repo location (https://github.com/loonwerks/INSPECTA-Open-Platform))

- SysMLv2 models (https://github.com/loonwerks/INSPECTA-Open-Platform/tree/main/ardupilot-basic/sysml)
- XML representation domain-scheduling version of the system (https://github.com/loonwerks/INSPECTA-Open-Platform/blob/main/ardupilot-basic/hamr/microkit/microkit.system)
- Python-based representation for the system description configuration for the MCS version of the generated system

Deliverables for first phases of development:

- proposals for SysMLv libraries for representing microkit concepts (following a style similar to HAMR's SysMLv2 AADL representation)
- documentation for the above explaining the rationale for the representation. The documentation should show excerpts of the XML and Python representations of a concept, and then the corresponding proposed representation in SysMLv2. The documentation should identify open issues and when needed, different options for the representation.
- worked examples of the SysMLv2 model representations for both the Isolette and Open Platform. Extensive inline documentation should be provided in these models to aid in backward traceability to the HAMR AADL sysmlv2 models and forward traceability to the microkit representations.
- A cleaned up version of these original instructions
- A roadmap for the next phases of development
- An enumeration of the long-term tooling (i.e., the "generating graphical visualizations" described above).

## 3. Repository access and launch

**HAMR Dev: Microkit SysML:** Got it. I'll load the HAMR dev knowledge first, then start a cloud agent on `hamr-sysml-microkit` to study the Microkit schema, the AADL libraries, and both examples before it drafts the libraries and docs.

_[A GitHub access card was shown because Cursor's GitHub app couldn't yet see the new repo.]_

**HAMR Dev: Microkit SysML:** Cursor's GitHub access can't see `santoslab/hamr-sysml-microkit` yet, probably because the repo is new and the santoslab install only covers selected repos. Could you add it using the card above? Once it's added, I'll start the Phase 1 agent with your full brief.

_[John granted access. Question: "I can see hamr-sysml-microkit now. Want me to start the Phase 1 cloud agent on it with your brief?" Options: Yes, start it / Not yet. John answered on the card: "Yes, start the Phase 1 agent"]_

**HAMR Dev: Microkit SysML:** Starting it now.

**HAMR Dev: Microkit SysML:** The [Phase 1 agent](https://cursor.com/agents/bc-d194da25-0dd3-5011-ab86-260090d67891) is running. It'll study the Microkit sources, the AADL libraries, and both examples, then open a PR with the libraries, design docs, worked models, cleaned-up requirements, and roadmap. I'll let you know when the PR is ready.

_[Cloud agent card: Phase 1: SysMLv2 library for seL4 Microkit system descriptions]_

## 4. Phase 1 result (PR #1)

**HAMR Dev: Microkit SysML** _(Sun Oct 25, 2026, 6:38 PM CT)_**:** Phase 1 is up for review in [PR #1](https://github.com/santoslab/hamr-sysml-microkit/pull/1). It includes four SysMLv2 packages written in the style of the AADL libraries, a design doc with XML, Python, and SysML excerpts side by side, worked models, the cleaned-up requirements, a roadmap, and the long-term tooling list. There are worked models for both Isolette and Open Platform, each with a domain-scheduling and an MCS variant.

The two scheduling flavors build different protection-domain structures, so I kept them as separate models rather than variants of one. The doc lays out both pipeline options and recommends starting with the read-only generated model, then allowing edits once a checker and translators exist. That's a suggestion for you to decide on, not a settled choice.

Here's what was checked. With your AADL library on the path, Sireum `4.20261021.b1efad5d` type-checks the library and all four examples. Element counts (protection domains, memory maps, channels) match the real XML and Python files. Nothing was translated back to XML or Python yet.

These are the questions for your team that matter most before writing translators:
- **Editing:** Should developers edit the Microkit model, and if so which fields? Examples are VM and device regions versus channel ids and domain lengths.
- **Open Platform schedule:** Its domain-scheduling schedule file isn't valid for the Microkit parser version the library follows, but Isolette's is. Which should the tooling target?
- **Open Platform guest VMs:** The XML and MCS outputs describe the guest VM differently, with different names, board addresses, and interrupt numbers.
- **Channels:** Should a channel be a connection between ports, as in AADL (what I did), or a system-level part closer to the XML?
- **Phase 2 representation:** Should the internal model extend HAMR's existing intermediate representation, or be a separate tree for system descriptions?

The full list is in `docs/design.md`. One more thing I found is a likely Sireum bug: the type checker crashes on `enum def` unless the AADL library is on the path. That's written up in `docs/verification.md`.

## 5. This transcript

**John** _(Mon Oct 26, 2026, 9:06 PM CT)_**:** Produce a transcript of this interaction that I can share with the rest of my team.  HAMR Infrastructure Dev bot just produced a transcript for me.  I would something similar for this session.

**HAMR Dev: Microkit SysML:** I'll start by looking at the transcript HAMR Infrastructure Dev made so this one follows the same format.

_[This file was delivered as the result.]_

---

## Outcomes

- **[PR #1](https://github.com/santoslab/hamr-sysml-microkit/pull/1)** (branch `cursor/sysml-microkit-library-7891`, 17 files): Phase 1 libraries, docs, and worked examples. Open for HAMR team review.
- **Library packages:**
  - `Microkit_Project`: base `Property`, enumerations, and limits taken from the Microkit parser (`Pd_Max_Id` 61, priority 254, stack bounds).
  - `Microkit_Properties`: one attribute definition per SDF attribute, with the parser default in its doc comment.
  - `Microkit`: `System`, `Protection_Domain`, `Memory_Region`, `Memory_Map`, `Channel` (a connection between `Channel_End` ports), `Irq`, `Virtual_Machine` / `Virtual_Cpu`, and the kernel `Domain_Schedule`.
  - `Microkit_HAMR`: pipeline tag, `Hamr_Trace`, `Hamr_Pd_Role`, the MCS user schedule, and the legacy Open Platform schedule. It's deliberately not named `HAMR_Microkit`, which already exists in `sysml-aadl-libraries` for AADL properties, and the two can be imported together.
- **Worked models:** Isolette and Open Platform, each in a domain-scheduling and an MCS variant (four models). Element counts were checked against Isolette `9591bdd` and Open Platform `cc73dd5`: 23/24/11/16 protection domains, 49/49/55/54 maps, and 22/22/10/10 channels.
- **Docs:** `docs/design.md` (rationale, side-by-side XML, Python, and SysML excerpts, Option 1 vs Option 2, traceability, open issues), `docs/verification.md`, the cleaned-up requirements, the roadmap, and the long-term tooling list.
- **Verification:** Sireum kekinian `4.20261021.b1efad5d`, installed with `scripts/install-sireum.sh`. `sireum hamr sysml tipe` accepts the library and all four examples when `sysml-aadl-libraries` is on the source path. The Microkit parser followed is microkit commit `39e7561`. The models haven't been translated back to XML or Python, and `hamr-tutorials` and `hamr-sysml-viz` examples weren't transcribed.
- **Additional open points:** sDDF `connect()` resources are only named in trace notes, not expanded. `sdfgen` 0.35.1 has no `smc`, `fpu`, `page_size`, or `region_paddr` setvar, and HAMR adds those by editing the XML, so the SysML follows the XML schema. Monitor child ids that `sdfgen` allocates are left unset on purpose.
