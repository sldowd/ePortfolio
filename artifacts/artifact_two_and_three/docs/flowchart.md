flowchart TD
    A(["User selects rescue type<br/>update_table fires, also at startup with None"])
    B["Fetch all records (db.read with an empty query)<br/>Build DataFrame, drop _id<br/>O(n)"]
    C{"Selection is a key<br/>in rescue_profiles?"}
    D["Look up profile criteria:<br/>breeds, sex, min_age, max_age"]
    E["score = 0"]
    F{"Breed in<br/>preferred list?"}
    F1["score += BREED_WEIGHT (40)"]
    G{"Sex matches<br/>preferred sex?"}
    G1["score += SEX_WEIGHT (30)"]
    H{"Age within<br/>min to max?"}
    H1["score += AGE_WEIGHT (30)"]
    H2["distance = gap to nearest bound<br/>score += max(0, 30 - distance)"]
    I["Store score in fit_score column"]
    K{"More animals?"}
    L["Keep rows where fit_score >= MIN_SCORE (70)<br/>O(n)"]
    M["Sort by fit_score, descending<br/>O(m log m)"]
    J["Return records to table<br/>Select row 0 (top-ranked animal)"]
    N["Table data feeds breed/age chart, map, and CSV export"]
    O(["End"])

    A --> B --> C
    C -- "No: None or Reset" --> J
    C -- Yes --> D --> E

    subgraph LOOP ["For each animal: O(n) total"]
        E --> F
        F -- Yes --> F1 --> G
        F -- No --> G
        G -- Yes --> G1 --> H
        G -- No --> H
        H -- Yes --> H1 --> I
        H -- No --> H2 --> I
        I --> K
        K -- "Yes: next animal" --> E
    end

    K -- "No: all scored" --> L
    L --> M --> J --> N --> O