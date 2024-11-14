# Analyzing HKU examination course types

## Retrieve data

Steps:

1. Proceed to <http://www.exam.hku.hk/tt_faclist.php> (`http`-only, disable HTTPS-only mode in your browser settings if needed)
2. Pick your favourite discipline
3. Copy the timetables without the reminders part at the end, e.g.:

    ```python
    BASc(AppliedAI) Examination Time Table for the First Semester of 2024-2025
    (As at Nov 13, 2024)
    Date  Time   Course Code  Description  Venue
    Dec 7 SAT  6:30 pm - 8:30 pm   ECON2280  Introductory econometrics  Rm 217 Main Bldg.
        Introductory econometrics  Rm 218 Main Bldg.
        Introductory econometrics  Rm 256 Main Bldg.
    Dec 9 MON  9:30 am - 11:30 am   CHIN1117  General introduction to classical Chinese language  Rm 5 Library Ext.
    Dec 9 MON  9:30 am - 11:30 am   FINA2320  Investments and portfolio analysis  3/F, Multi-purpose Zone, Main Library
        Investments and portfolio analysis  CPD-LG.07-10, Centennial Campus

    (...)

    There are changes in time, venue or special note for those courses in red color and bold. Details of the changes made can be found at the Examinations Office website (www.exam.hku.hk) under the section "amendments to timetable".
    Note: All in-person examinations are close-book examinations, unless otherwise specified.

    Electronic Calculators

    # Copy till here
    ```

4. Paste the content into a new `.txt` file
5. Run the `bash` command below, you will see an result like this:

    ```bash
    123er@Eric  /d/Personal Data/Repositories/personal-repo/misc/hku-examinations (main)
    $ cat 2024-sem1/ai.txt | grep -E "[A-Z]{4}" --only-matching | sort | uniq -c | sort -r
        17 COMP
        9 STAT
        8 MATH
        4 FINA
        3 IMSE
        3 GEOG
        3 ECON
        3 APAI
        2 SOCI
        2 PHYS
        2 CUND
        2 CHIN
        2 CCST
        1 URBS
        1 PSYC
        1 MECH
        1 IIMT
        1 CSCI
        1 CCGL
        1 BUSI
        1 BSTC
        1 BIOL
        1 ACCT

    123er@Eric  /d/Personal Data/Repositories/personal-repo/misc/hku-examinations (main)
    $
    ```

## Shell command

```bash
cat <your_new_text_file>.txt | grep -E "[A-Z]{4}" --only-matching | sort | uniq -c | sort -r
```

Run on *all* of the text files come with this repository:

```bash
cat **/*.txt | grep -E "[A-Z]{4}" --only-matching | sort | uniq -c | sort -r
```

## Important things to consider in this data analysis

* Only courses with examinations were appeared on the website
* The result only shows the ***diversity*** of type of courses student enrolled into, but not the ***majority*** of students enrolled into

## Sidenote when trying to collect new datas

* Previous semester examinations data will ***disappear*** after some time
* Current semester data *only* appear after the examination timetable has been announced for the majority of students (typically around the *end of October* for *semester 1*)
