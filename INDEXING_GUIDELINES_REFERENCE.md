# USC Shoah Foundation - Biographical Indexing Guidelines Reference

Quick reference guide for indexing Jewish survivor testimonies. Based on sections 2.4-2.6 of the official guidelines.

---

## 2.4 Entry Info

**Purpose:** Record indexer information and initial metadata for the session.

### Fields

| Field | Type | Format | Notes |
|-------|------|--------|-------|
| **Initials** | Text | Your 2-3 letter initials | Entered once per session |
| **Date** | Date | `MMM D, YYYY` (e.g., `Aug 8, 2013`) | No period after month abbreviation |
| **Language (PIQ)** | Dropdown (Multi-select) | Selected from choice group | Language of Pre-Interview Questionnaire and answers |

### Special Notes
- Only filled out once when starting the process
- If PIQ was in a different language, add it via the "Add" button to these fields

---

## 2.5 Interviewee Info

Biographical section for the main interviewee. The section name varies by experience group (e.g., "Jewish Survivor Info").

---

### 2.5.1 Interviewee Name(s), Gender, Date of Birth

**Purpose:** Record primary demographic information.

**Entry Method:** Double-click the field → Select "Person Information" → Fill in data

#### Fields in Person Information Dialog

| Field | Type | Format | Rules |
|-------|------|--------|-------|
| **First Name** | Text | As given | Pre-assigned; verify against PIQ |
| **Middle Name** | Text | As given | Leave blank if none |
| **Last Name** | Text | As given | Pre-assigned; verify against PIQ |
| **Gender** | Dropdown | Male / Female / Unknown | Only if certain; many names are not gender-specific |
| **Date of Birth** | Date | See date formats below | Verify during video viewing |
| **Relation to Interviewee** | Dropdown | Pre-set to "Interviewee" | Cannot be changed |
| **Survivor Status** | Dropdown | Yes / No / Unknown | See 2.5.4 for definitions |

---

### 2.5.2 Dates - Format Rules

**Standard Format:** `MMM D, YYYY` (e.g., `Oct 24, 1925`)

#### Special Cases

| Scenario | Format | Example |
|----------|--------|---------|
| Month and Year only | `MMM YYYY` | `Aug 2013` |
| Multiple birth dates | Separated by "or" | `Jun 4, 1925 or Jun 7, 1925` |
| Date range | Separated by "or" in single field | `1942 or 1943` |
| Multiple months | Two distinct dates | `May 4, 1942 or Jun 4, 1942` |
| Season indicated | Unabbreviated, lowercase season | `summer 1944` (no apostrophe) |
| Decade | No apostrophe | `1960s` |
| Estimated/approximate | `@` symbol with space | `@ 1994` or `@ 1918` |
| Age at death calculation | Use `@` for calculated birth year | If "13 years old when died in 1943", enter `@ 1930` |
| Events/holidays | Direct transcription | `Rosh Hashanah 1944` |
| Hebrew calendar dates | Direct transcription + research | `25 Tamuz 5696` → Research in Encyclopaedia Judaica, enter both: `21 Kislev, 5400 – Jun 6, 1987` |
| Time period qualifiers | Prefix with descriptor | `beg 1939`, `mid Jun 1939`, `end 1939` |
| Decade qualifier | Include qualifier | `early 1960s`, `late 1970s` |
| Prewar/Wartime/Postwar | Standard terms | `prewar`, `wartime`, `postwar` |

**Date Entry Order:** Month always enters first

---

### 2.5.3 Gender

**Type:** Dropdown or text field

**Guidelines:**
- Only indicate if **certain**
- Many names are not gender-specific
- Verify during video viewing if uncertain
- Leave blank if unsure

---

### 2.5.4 Genocide/Mass Violence Survivor (Yes/No/Unknown)

**Purpose:** Determine if interviewee meets survival criteria for the testimony's event group.

#### Holocaust Survivor Definition (Jewish Survivors)

A Holocaust survivor is anyone who:
- Suffered and survived persecution for **racial, religious, sexual, physical, or political reasons** while under Nazi or Axis control between **1933 and May 8, 1945**, OR
- Was **forced to live clandestinely**, OR
- Had to **flee Nazi/Axis control** during the war to avoid imminent persecution

**Survivor Status Criteria:**
- Person was **alive at point of liberation** and/or **May 8, 1945**, OR
- Person **died before May 8, 1945** but **successfully fled** from German/Axis countries

**Examples of Survivors:**
- German Jews fleeing Germany before the war
- Jews from eastern Poland who fled to Soviet territory after Sep 1, 1939 (before June 1941 German invasion)
- Non-Jewish groups: gay men, Jehovah's Witnesses, disabled persons, Sinti and Roma, political prisoners, non-Jewish Poles (intellectuals, clergy)

**Axis Countries - Special Dates:**
| Country | Date Anti-Jewish Legislation Appeared |
|---------|---------------------------------------|
| Italy | 1938 |
| Romania | 1938 |
| Hungary | 1938 |
| Bulgaria | 1940 |
| Czechoslovakia | 1939 |
| Yugoslavia | 1941 |

---

### 2.5.5 Names and Aliases

#### 2.5.5.1 First, Middle, and Last Names (Person Information)

**Location:** Person Information pop-up box (accessed via double-click)

**Guidelines:**
- Interviewee's name is pre-assigned before Bio Indexing begins
- If discrepancy between pre-assigned name and PIQ/documentation spelling, follow **Release Name rules** (see 2.5.5.3)
- Fields pre-filled: First, Middle, Last Name

---

#### 2.5.5.2 Aliases

**Purpose:** Make additional names and spelling variations searchable.

**Definition:** Any additional names or spelling variations found in:
- Accompanying paperwork, OR
- Stated during audiovisual interview

**Entry Method:**
1. Double-click on interviewee record
2. Select "Aliases" option
3. Click OK
4. Enter all names and aliases

---

#### 2.5.5.3 Release Name

**Definition:** The spelling of the interviewee's name as it appears on the **Release Agreement** (the legal document the interviewee signs, also called Consent Form).

**Importance:** Release Name is the **official name** by which the interviewee should be referred.

#### Release Name Principles

| Principle | Guideline |
|-----------|-----------|
| **Legible Signature** | Signature spelling likely reflects interviewee's wishes |
| **Release Agreement Match** | Must match Release Agreement exactly |
| **Alignment with Main Name** | Ensure Release Name = Main Interviewee Name when possible |
| **Diacritics** | Faithfully render all diacritics (é, ñ, etc.) |
| **Non-Roman Scripts** | Transliterate using Library of Congress Romanization Tables |

#### Non-Roman Script Handling

| Scenario | Action |
|----------|--------|
| Release Form has non-Roman original AND Roman version | Prefer non-Roman transliteration for Release Name; enter Roman version in Other Names field |
| Interviewee specified preferred transliteration | Honor specified transliteration as Release Name; enter LOC transliteration as alias |
| No preferred transliteration specified | Use LOC transliteration as Release Name |
| Other unknown transliterations (from interviewer, etc.) | Enter as Other Names |

**LOC Note:** When using Library of Congress transliteration, write `(LOC)` in the Notes field associated with the name.

#### Contact Archivist If:
- Release Agreement affirmed with only fingerprint
- Interviewee wrote inscriptions on Release Agreement specifying alterations
- No Release Agreement associated with testimony

---

#### 2.5.5.4 Other Aliases

**Purpose:** Capture name variations across different contexts and time periods.

#### Alias Types and Rules

| Alias Type | Rules | Example |
|------------|-------|---------|
| **Name at Birth** | Equivalent to "Given Name" on some PIQ versions | Hebrew name at birth |
| **Last Name During War** | World War II period (Sep 1, 1939 – May 8, 1945 Europe; Sep 2, 1945 Asia/Shanghai). **Last name only** | If maiden name changed during war |
| **Current Last Name** | Some PIQ ask for this; **last name only** | Married name after war |
| **Maiden Name** | Do NOT assume maiden name = name at birth. If clear but not explicitly given, enter in square brackets | `[Goldstein]` if maiden name clear but not stated |
| **Presumed Names** | Put in square brackets `[ ]` | `[Cohen]` if presumed last name |
| **False Name** | Name used under false identity | `Maria Kowalski` (false Christian name) |
| **Hebrew Name** | All parts entered in First Name field only | `Abraham ben Moshe` all in first name |
| **Other Name** | For additional variations; can include explanation in Notes field | Various spellings of surname |

#### Naming Conventions

| Situation | Format | Example |
|-----------|--------|---------|
| **Unverified Spelling** | Use `*` after name | `Rosenberg*` |
| **Presumed Name** | Square brackets | `[Smith]` |
| **No Title, Only Name** | Do not add people with only titles | Don't add entry for "maid" alone |
| **Can Presume Last Name** | Person can be created; presumed last name in brackets | Brother of interviewee with only first name known |
| **Multiple Same-Named People** | Use underscore numbering | `Brother: Mr. Smith`, `Brother: Mr. Smith_1`, `Brother: Mr. Smith_2` |
| **Family Surnames Only** | Include "family" in last name field | `Smith family` in Last Name field |

---

### 2.5.6 City of Birth

**Type:** Indexing Term (choice group dropdown)

**Entry Method:** Search Indexing Term Choice Group → Press "Add" button

#### Guidelines

- Be **specific and accurate** while remaining true to PIQ/documentation integrity
- Conduct **thorough search** of choice group
- **Double-click** specific terms to read definitions and synonyms
- If uncertain, **propose new term** rather than assume existing one is correct

#### Proposing New Indexing Terms

**Format:** `City: Name of City (Country)`

**Examples:**
- `City: Freising (Germany)`
- `Ghetto: Cernauti (Romania : Ghetto)`
- `Camp: Dachau (Germany : Concentration Camp)`

**Best Practices:**
- Include comments like "phonetic spelling" or "near XYZ city in Poland"
- Copy proposed term text to plain text field underneath

---

### 2.5.7 Country of Birth

**Type:** Indexing Term (choice group dropdown)

**Entry Method:** Search choice group → Press "Add" button

#### Key Principle
Select country **based on borders as they existed at time of person's birth**, not modern borders.

#### Special Countries - Historical Border Changes

Always check the **timeline in the city's term definition** to determine correct country term.

##### Post-WWI Changes (Default: November 11, 1918)

| Given Country | Date | Indexing Term to Use | Plain Text Entry |
|---------------|------|----------------------|------------------|
| Austria | ≤Nov 10, 1918 | Austria-Hungary (historical) | Austria |
| Czechoslovakia | ≤Nov 10, 1918 | Austria-Hungary (historical) | Czechoslovakia |
| Hungary | ≤Nov 10, 1918 | Austria-Hungary (historical) | Hungary |
| Poland | ≤Nov 10, 1918 | Check city timeline (Austria-Hungary or Russian Empire) | Poland |
| Romania | ≤Nov 10, 1918 | Check city timeline (Romania, Austria-Hungary, or Russian Empire) | Romania |
| Yugoslavia | ≤Nov 10, 1918 | Check city timeline | Yugoslavia |

##### Russian Empire → Soviet Union

| Period | Indexing Term |
|--------|----------------|
| Until Dec 29, 1922 | Russian Empire (historical) |
| Dec 30, 1922 onwards | Union of Soviet Socialist Republics (historical) |

**Special Cases - Eastern European Territories:**
- **Belorussia/Belarus/White Russia:** Use Russian Empire until Nov 10, 1918; then check city timeline for Poland or Russia (until Dec 30, 1922); then USSR
- **Ukraine:** Use Russian Empire or Austria-Hungary (check city timeline); post-Nov 10 check for Poland or Russian Empire (until Dec 30, 1922); then USSR
- **Armenia/Azerbaijan/Georgia:** Use Russian Empire until May 26, 1918. After: continue indexing as these countries until independence loss (April/December 1920, March 1921); then USSR from Dec 30, 1922

##### Ottoman Empire to Turkey

| Period | Indexing Term |
|--------|----------------|
| Until Oct 28, 1923 | Ottoman Empire (historical) |
| After Oct 28, 1923 | Turkey (or other country) |

**Special Case - Syria before 1922:** Use Ottoman Empire (historical); enter "Syria" in plain text

##### Rwanda - Pre-Independence

| Date | Indexing Term | Plain Text |
|------|----------------|-----------|
| ≤Jun 30, 1962 | Ruanda-Urundi | Rwanda |

---

### 2.5.8 Religious Identity

**Type:** Indexing Term (choice group dropdown)

**Entry Method:** Search choice group → Press "Add" button

#### Guidelines

- **Time periods:** Prewar, Postwar, Unknown (time period unknown rarely used)
- **Default to most specific term:** Don't index both "Judaism" and "Hasidism" — use "Hasidism"
- Even more specific is better: e.g., "Aleksandrów Hasidism" > "Hasidism"
- **"None" and "Non-applicable":** Only use if actual answers on documentation; don't substitute for blank fields
- **Propose new terms** if needed; copy to plain text field

---

### 2.5.9 Flight

**Question:** Did the interviewee flee from a territory under Nazi control (or from Rwanda after April 7–July 4, 1994)?

**Type:** Dropdown

**Values:** Yes / No / (leave blank)

**Purpose:** Ascertain if fleeing from persecution is a central part of testimony experience.

**Related Topic:** For more details, see Video Indexing guidelines on "forced movement/flight"

---

### 2.5.10 Ghettos, Camps, Prisons

**Questions:**
- Name(s) of ghetto(s) in which interviewee was forced to reside?
- Name(s) of camp(s) in which interviewee was incarcerated?
- Name(s) of prison(s) in which interviewee was incarcerated?

**Type:** Indexing Term (multi-select)

**Entry Method:** Search choice group → Press "Add" button (accepts multiple entries)

#### Camps Field - Inclusions

The "Camps" field **should contain:**
- Concentration camps
- Prisoner-of-war camps
- Internment camps
- Forced labor camps
- (Includes WWI Ottoman camps and WWII Nazi/Axis camps)

#### Camps Field - Exclusions

The "Camps" field **should NOT contain:**
- Temporary forced labor battalion encampments (e.g., Hungary, WWII)
- Allied internment camps (WWI or WWII)
- Allied refugee camps (WWI or WWII)
- Allied displaced persons camps

**Workaround:** For excluded camps, index experiential terms in "Special Experiences/Situations" question instead.

#### Generic Terms

Use indexing terms with `(generic)` suffix when more specific location cannot be determined.

**Example:** `Auschwitz (Poland: Concentration Camp)(generic)` when unable to distinguish Auschwitz I, II, or III

#### Proposing New Terms

If term not found, propose it and copy to plain text field underneath.

**Related Topic:** See Video Indexing guidelines on "Restricted Housing" and "Incarceration"

---

### 2.5.11 Massacres

**Questions:**
1. Did the interviewee escape from a mass execution or killing site?
2. If yes, what was the location?

**Type:** Yes/No dropdown + Indexing Term

**Entry Method:**
1. Double-click "Did interviewee escape?" field → Select Yes/No or leave blank
2. If Yes: Index name of massacre location from choice group
3. Add button to select location
4. If term not found, propose it; copy to plain text field

**Related Topic:** See Video Indexing guidelines on "Massacres"

---

### 2.5.12 Hiding/Identity Concealment

**Questions:**
1. Did the interviewee go into hiding at any point during the war?
2. Where was the person hiding or under false identity?
3. Type of hiding place?

**Type:** Yes/No dropdown + Indexing Terms (multi-column)

#### Entry Method

1. Double-click "Did interviewee go into hiding?" → Select Yes/No or leave blank
2. If Yes: Enter hiding locations and types

#### Multiple Locations Rule

**Use one column per geographic location; use multiple "type of hiding place" entries within each column:**

**Correct:**
- Column 1: City = Lodz; Type = farms, hospitals

**Incorrect:**
- Column 1: City = Lodz, Type = farms
- Column 2: City = Lodz, Type = hospitals

**To add new column:** Click the "+" sign at top of form

#### Special Cases

| Situation | Action |
|-----------|--------|
| Living under false identity | Leave "type of hiding place" **blank** (doesn't apply) |
| Living under false identity anywhere | Index "identity concealment" in Special Events/Situations field |

**Related Topic:** See Video Indexing guidelines on "Hiding and Identity Concealment"

---

### 2.5.13 Resistance

**Questions:**
1. Was the interviewee involved with any underground, resistance, or partisan groups?
2. Name of resistance group(s)?

**Type:** Yes/No dropdown + Indexing Term

#### Entry Method

1. Double-click "Was interviewee involved?" → Select Yes/No or leave blank
2. If Yes: Enter resistance group name(s) from choice group

#### Resistance Group Rules

- Enter **only resistance groups relevant to Holocaust/genocide in question**
- **Exception:** Jewish resistance groups in Palestine can and should be indexed
- For unnamed groups (e.g., Rwanda): Mark Yes but leave "name of resistance group" **blank**
- If term not found, propose it; copy to plain text field

**Related Topic:** See Video Indexing guidelines on "Resistance"

---

### 2.5.14 Forced Marches

**Question:** Was the interviewee on any forced/death marches?

**Type:** Dropdown

**Values:** Yes / No / (leave blank)

**Entry Method:** Double-click answer field → Select option

---

### 2.5.15 Liberation

**Questions:**
1. Who liberated you? (Armed force or resistance group)
2. Where were you liberated?

**Type:** Indexing Term (two separate fields)

#### Who Liberated

Select name of liberating armed forces or resistance group from choice group.

**Special Note - Rwanda:** Survivors usually refer to "RPF" but the correct indexing term is **"RPA" (Rwandan Patriotic Army)**

#### Where Were You Liberated

Index the location from choice group.

**If term not found:** Propose it; copy to plain text field

**Related Topic:** See Video Indexing guidelines for more details

---

### 2.5.16 Other Attributes

**Purpose:** Capture additional experiential roles beyond primary experience group.

Although each interviewee has one primary experience category (Jewish Survivor, Liberator, etc.), many people had alternate roles during the Holocaust.

**Use this field** to convey additional experiential roles.

**Examples:**
- Jewish survivor who also acted as a rescuer
- Liberator with other significant roles

---

### 2.5.17 Special Events/Situations

**Purpose:** Capture interviewee experiences not asked elsewhere.

**Type:** Indexing Term (multi-select, choice group only)

**Entry Method:** Search choice group → Select all pertinent terms

#### Allowed Terms (Examples)

Choice group includes terms such as:
- Identity concealment
- Displaced person camps
- Kindertransport
- Camp medical experiments
- Camp escapes
- Prisons
- (And others per choice group)

#### Guidelines

- Select **all pertinent terms** from choice group
- Do **NOT propose new terms** for this field
- Check documentation one last time against choice group
- During video viewing, select additional terms if testimony indicates additional experiences in the choice group

---

## 2.6 Family/People in this Testimony

**Purpose:** Record all people mentioned in PIQ or audiovisual interview.

**Entry Method:** Family/People Testimony Spreadsheet

**Importance:** Once entered in Bio Indexing, names become immediately available for indexing in Video Indexing segments.

---

### 2.6.1 Names

**Rules:** Follow same rules as interviewee names with these differences:
1. You must enter the person's **Main Name yourself** (not pre-assigned)
2. There is **no Release Name** to enter

#### Additional Rules for Family/People Names

| Rule | Format | Example |
|------|--------|---------|
| Unverified spelling | Use `*` after name | `Rosenberg*` |
| Presumed names | Square brackets | `[Cohen]` |
| Don't add title-only entries | Skip | Don't enter "maid" without name |
| Person known by last name only | Can create if relationship known | Include relationship to make it allowable |
| Can presume last name | Create with presumed last name in brackets | Brother `[Smith]` if last name presumed |
| Multiple same-named people | Underscore numbering | `Brother: Mr. Smith`, `Mr. Smith_1`, `Mr. Smith_2` |
| Family surnames only | Include "family" | `Smith family` in Last Name field |
| Hebrew name | All parts in First Name field only | `Abraham ben Moshe` in First Name |
| Only first name known | Allowable if relationship known | Include relationship field |
| Do NOT enter unless stated | No aliases unless explicitly documented | Skip speculative aliases |

#### Non-Roman Character Sets

**Priority Order:**

1. **If interviewee specified preferred transliteration:** Honor it; use ALA-LC as alias
   - Write `(LOC)` in Notes field for ALA-LC version
   
2. **If no preferred transliteration:** Use ALA-LC Romanization Tables (Library of Congress)
   - Write `(LOC)` in Notes field
   
3. **All other transliterations** (by unknown persons): Enter as Other Names

**Source:** ALA-LC Romanization Tables at Library of Congress website

#### Children's Names

**A child is defined as ≤13 years old. If age unknown, do not enter as child.**

| Situation | Entry Format |
|-----------|--------------|
| Baby's last name only | "baby" in First Name field (not Title field) |
| Male child's last name only | "Master" in Title field |
| Female child's last name only | "Miss" in Title field |

#### Gender and Dates

See sections 2.5.2 and 2.5.3 for date formats and gender guidelines (same rules apply).

---

### 2.6.2 Relationship to Interviewee

**Type:** Dropdown (pre-defined relationship categories)

#### Core Principles

| Principle | Guideline |
|-----------|-----------|
| **Do not presume biological** | Unless explicitly stated in PIQ, documentation, or testimony |
| **Define correctly** | Base on original/primary way interviewee came into contact |
| **Prewar takes precedence** | If prewar relationship exists, prefer over wartime (e.g., friend not "aid giver") |
| **Familial always first** | Family relationships supersede all other roles |

#### Specific Rules

| Relationship Type | Rule |
|-------------------|------|
| **Maternal/Paternal** | Only use qualifiers when there is **direct family relationship**. Aunts/uncles by marriage = "uncles" only (not "paternal uncles") |
| **Divorced Spouse** | Use "husbands, ex" or "wives, ex" |
| **Deceased Spouse** | Use "husbands" or "wives" |
| **Deceased Ex-Spouse** | Use "husbands, ex" or "wives, ex" |
| **Spouse Not Actually Married** | If PIQ lists person under spouse but not actually married: Create as "Other People" with relationship "friends" |
| **Extended Family** | 2nd, 3rd cousins and beyond = "extended family members" |

---

### 2.6.3 Cause of Death

**Type:** Dropdown (multi-option for non-interviewees only)

**Applies to:** Family/people other than the interviewee

#### Options and Definitions

| Option | Definition | Notes |
|--------|------------|-------|
| **Holocaust-related death** | Deaths directly or indirectly caused by Holocaust | Can be immediate post-WWII or years later from related causes. Survivor can also die Holocaust-related death. **Must be explicitly attributed** in PIQ, documentation, or testimony. |
| **Rwandan Tutsi Genocide-related death** | Deaths directly or indirectly caused by 1994 Rwandan Tutsi Genocide | Can be immediate post-genocide or years later from related causes. Survivor can also die genocide-related death. **Must be explicitly attributed**. |
| **Interviewee does not know** | Used when stated in PIQ, documentation, or testimony | Only use if explicitly stated |
| **Natural death** | Diseases, illnesses, cancer, stroke, Alzheimer's, AIDS, etc. | Covers most non-violent deaths |
| **Other type of death** | Unnatural, non-genocide-related | Car crash, suicide, skiing accident, non-genocide drowning/murder, etc. |
| **Not specified** | When none of above can be determined | Use as fallback when unclear |

#### Key Note
"Holocaust-related death" can apply to survivors who died years after the war from related causes — but death **must be explicitly attributed** to the Holocaust in source material.

---

### 2.6.4 Survivor (Yes/No/Unknown)

**Type:** Dropdown

#### Check "Yes" When:
- PIQ, documentation, or audiovisual interview **clearly indicates** the person is a survivor

#### Check "No" When:
- Person **died before or during** the genocide
- Person **could not have been survivor** per methodology (died before genocide, born after, perpetrators, etc.)

#### Check "Unknown" When:
- **Survivor status cannot be determined**

---

### 2.6.5 Place of Birth (Non-Interviewees)

**Type:** Indexing Term (location fields)

**Entry Method:** Select relevant Location Type → Click Place Name/City/Town/Village/Country field

#### Location Type Selection

- **Usually:** "places – general"
- **Other options:** When context indicates specific location type

#### Available Fields

| Field | Contains |
|-------|----------|
| **Place Name** | Camps, ghettos, provinces, voivodships, oblasts, etc. |
| **City/Town/Village** | Cities or kibbutzim |
| **Country** | Countries |

**Approach:** Apply same geographic logic as Interviewee City of Birth and Country of Birth (see 2.5.6–2.5.7)

#### Proposed Terms - Comments

For all proposed terms for cities of birth, include relevant comment in Comment field:

**Format:** `POB + Location + DOB`

| Example | Format |
|---------|--------|
| Mother's place of birth | `POBM 1896` (POB + M + DOB) |
| Father's place of birth | `POBF 1888` (POB + F + DOB) |
| Sibling's place of birth | `POBSChana 1913` (POBS + Name + DOB) |
| Interviewee place of birth | `POBI 1912` (POB + I + DOB) |

---

### 2.6.6 Place of Death (Non-Interviewees)

**Type:** Indexing Term (location fields)

**Entry Method:** Similar to Place of Birth, but Location Type often differs

#### Location Type Selection

Usually **NOT "places – general"** — often something more specific:
- Concentration camps
- Ghettos
- Other relevant location type

**Check source material** (PIQ, documentation, testimony) for context

#### Important Note on Camps as Cities

Older PIQ versions ask for "city" in Place of Death. In Holocaust context, usually safe to enter written city as a camp if dates and facts apply.

**Example:** If "Dachau" listed as city of death for family member not from Dachau, typically safe to enter "Dachau Concentration Camp"

#### Proposed Terms - Comments

For all proposed place of death terms, use comment format:

| Example | Format |
|---------|--------|
| Any place of death | `POD` |

---

### 2.6.7 Common Abbreviations

#### d/k – "Interviewee Does Not Know"

**For indexing term answers:**
- In questions regarding camps/ghettos when "d/k" appears: Enter either "d/k" or phrase "interviewee does not know" as plain text answer

**For personal information:**
- Using Person Information box, indicate in "notes about this person" or "specific location" fields
- **Do NOT enter "d/k" in name fields** — leave blank instead
- **Example:** If "First Name: d/k. Last Name: Jones" → Leave First Name blank; in notes write "Ezekiel Smith does not know Mr. Jones' first name"

#### n/a – "Not Applicable"

- Enter "n/a" or phrase "not applicable" in plain text field for that answer
- Use only when explicitly stated on documentation

#### ? – Question Mark

- Do **NOT enter "?"** into answer field
- Use personal judgment:
  - Enter "n/a", OR
  - Write text like "Ezekiel Smith is not sure", OR
  - Leave blank

#### Geographic Location - Uncertainty

**When documentation indicates uncertainty about location:**
- Use phrase in plain text: `"probably (location name), but Ezekiel Smith is not sure"`
- Do **NOT use indexing term** at this stage
- Try to determine precise location after listening to audiovisual interview

---

### 2.6.8 Addendum: Name Changes

**Critical Principle:** Release name must match Release Agreement exactly.

#### Pre-Entry Verification

- Ensure pre-set interviewee name (auto-displayed) is correct
- If multiple release forms attached: Use **most current form** as official document

#### Permissible Name Changes (with Solution)

| Problem | Solution | Example |
|---------|----------|---------|
| Missing diacritics in database but on Release Agreement | Add diacritics | Diacritics added to match |
| First/last name reversed on Release Agreement | Enter correctly | Correct order in database |
| Both names in last name field on Release Agreement | Split correctly | First name → First field; Last name → Last field |
| Generational distinctions (Jr., IV) on Release Agreement but not in database | Add generational distinctions | "Smith Jr." in last name field |

#### Family Member Release Form Error

**Problem:** Release Agreement filled out by family member with own information

**Solution:** New Release Agreement sent to survivor for correct information

#### Parenthetical Information

| Type | Problem | Solution |
|------|---------|----------|
| **Diminutive after first name** | Richard (Ricky) | Don't add diminutive to release name; add as alias |
| **Alternate versions of last name** | Romanovski (Romanov) | Don't add parenthetical; add as alias |

#### Signature Mismatch

**Problem:** Legible signature clearly doesn't match release name written in boxes

**Solution:** Contact interviewee before changing; if not possible, written name in boxes prevails

#### Different Spelling in Testimony vs. Release Agreement

**Problem:** Interviewee spells name differently in testimony than on Release Agreement

**Solution:** Release Agreement spelling prevails; create alias for testimony spelling

#### Alternate Spelling Throughout Documentation

**Problem:** Release name one way on Release Agreement; alternate spelling in other documentation

**Solution:** Release Agreement spelling prevails; create aliases for all other spellings

#### Multiple Release Names

**Problem:** More than one release name on Release Agreement

**Solution:** Only ONE release name per interview; all others become aliases

#### Duplicate Names on Release Agreement

**Problem:** Both maiden and married names in last name field; maiden name also in release maiden name field

**Solution:** Release Agreement governs what is entered, even if duplicated

---

### 2.6.9 Exiting the Biographical Profile Application

**When finished or taking a break:** Exit testimony or log out

#### Exit Options

| Option | Action |
|--------|--------|
| **Stay in Application** | Select "Testimony Selection Page" (logged in, different testimony) |
| **Exit Completely** | Select "Log Out" |

#### Status Assignment (Required)

**Must assign status from dropdown before exiting:**

| Status | Meaning |
|--------|---------|
| **PIQ data entry in progress** | Still entering information for interviewee only |
| **PIQ data entry end** | Finished entering interviewee information only |
| **PIQ index in progress** | Still entering information for interviewee AND family/people |
| **PIQ index end: no PKW** | Finished interviewee + family/people; **no proposed terms**. Also implies video indexing complete and relevant info added to Bio. |
| **PIQ index end: PKW** | Finished interviewee + family/people; **proposed terms exist**. Also implies video indexing complete and relevant info added to Bio. |

**PKW = Proposed Keyword(s)**

#### Additional Problem Flags

If additional problems noticed, select relevant choice from dropdown:

**Example:**
- If no Release Form: Select "(prob) no release form"

---

## Quick Reference: Data Type Summary

| Data Type | Entry Method | Multi-select? |
|-----------|--------------|---------------|
| **Text** | Direct keyboard input | No |
| **Date** | Text input with format rules | No |
| **Dropdown** | Click field, select from list | No |
| **Indexing Term** | Search choice group, "Add" button | Yes |
| **Checkbox (Yes/No/Unknown)** | Double-click, select option | No |

---

## Common Format Checklist

- [ ] Date format: `MMM D, YYYY` (no period after month)
- [ ] Multiple values: Separated by "or" or in separate columns
- [ ] Estimated dates: `@ 1994` (space after @)
- [ ] Presumed names: Square brackets `[Name]`
- [ ] Unverified spelling: Asterisk after `Name*`
- [ ] Foreign transliteration: Note `(LOC)` in Notes field
- [ ] Proposed indexing terms: Formatted correctly with country/type in parentheses
- [ ] Relationship: Based on primary/original contact, not presumed
- [ ] Geographic terms: Based on borders at time of birth/death
