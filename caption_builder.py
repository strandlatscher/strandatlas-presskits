#!/usr/bin/env python3
# STRANDATLAS · CAPTION-BUILDER  (kanonisch, persistiert 08.11.2026)
# Erzwingt das Caption-GERÜST; die kreative Mitte (Hook, Body, Frage, 5. Hashtag)
# bleibt pro Haus Eingabe — der Builder erfindet KEINE Prosa.
#
# KANON (pro Woche fünf Captions; der Story-Teaser bekommt KEINE Caption —
#        er wird über Sticker/Tag bespielt):
#   Carousel · Reel Vorstellung · Reel Ankommen · Reel Im Detail · Reel-fast Finale
#
# AUFBAU je Caption:
#   Anzeige
#   <Hook — eine kurze Zeile, endet mit Punkt>
#   <Body — 3–5 Sätze, schließt mit „Kein X, kein Y — nur …“>
#   <Ort>, <Land>.
#   <Engagement-Frage?>
#   Folge @strandatlas für stille Häuser am Meer — jede Woche ein neues Porträt.
#   Speichere dir das für die nächste große Reise und <teilen>. Das ganze Porträt: Link in unserer Bio.
#   #strandatlas #<haus> #<ort> #<land> #<thema>
#   (Finale zusätzlich: Bookend-Tag @<handle> — Wochenauftakt wird über die Story getaggt)
#
# REGELN:
#   * „Speichere dir" (nie „Speicher dir").
#   * <teilen> wechselt zwischen „teile es mit …" und „schicke es …" (Abwechslung).
#   * Hashtags: genau 5, lowercase; Haus/Ort/Land automatisch aus Eingaben kleingeschrieben.
#   * Bookend-Tag @<handle> nur am Finale (Story trägt den Auftakt-Tag via Sticker).
#   * Absätze durch Leerzeile getrennt; Ausgabe passt 1:1 in die Plan-Spalte „Caption (fertig)".
ANZEIGE="Anzeige"
FOLGE="Folge @strandatlas für stille Häuser am Meer — jede Woche ein neues Porträt."
SAVE_PRE="Speichere dir das für die nächste große Reise und "
BIO="Das ganze Porträt: Link in unserer Bio."
POSTS=("carousel","vorstellung","ankommen","im_detail","finale")

def _slug(s):
    return "".join(ch for ch in s.lower().replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss") if ch.isalnum())

def _hashtags(handle, ort, land, thema):
    # handle ohne @, thema ohne #
    return f"#strandatlas #{_slug(handle)} #{_slug(ort)} #{_slug(land)} #{_slug(thema)}"

def build_caption(hook, body, ort, land, frage, teilen, handle, ort_tag, land_tag, thema, bookend=False):
    """teilen = vollständige Verbphrase, z.B. 'teile es mit deiner Reisecrew' ODER 'schicke es deinem Reisebuddy'."""
    parts=[ANZEIGE, hook.strip(), body.strip(), f"{ort}, {land}.", frage.strip(),
           FOLGE, f"{SAVE_PRE}{teilen.strip()}. {BIO}", _hashtags(handle, ort_tag, land_tag, thema)]
    cap="\n\n".join(parts)
    if bookend: cap += f"\n\n[Bookend-Tag: @{_slug(handle)}]"
    return cap

def build_all(haus, handle, ort, land, hooks, bodies, fragen, teilen, themen, ort_tag=None, land_tag=None):
    """hooks/bodies/fragen/teilen/themen: dicts mit Keys aus POSTS. Gibt {post: caption} für die 5 Posts.
    Der Story-Teaser ist bewusst NICHT enthalten (keine Caption)."""
    ot = ort_tag or ort; lt = land_tag or land
    out={}
    for p in POSTS:
        out[p]=build_caption(hooks[p], bodies[p], ort, land, fragen[p], teilen[p],
                             handle, ot, lt, themen[p], bookend=(p=="finale"))
    return out

def to_markdown(haus, handle, region_label, caps, slide_order, teaser_motiv):
    H={"carousel":"Carousel · Di 20:00","vorstellung":"Reel „Vorstellung“ · Mi 12:30",
       "ankommen":"Reel „Ankommen“ · Do 08:30","im_detail":"Reel „Im Detail“ · Fr 21:00",
       "finale":"Reel „Finale“ (Best-of) · So 11:00"}
    md=[f"# {haus} — Instagram-Captions",
        f"\nHandle: **@{_slug(handle)}** · {region_label}",
        "Stil: Strandatlas-Caption-Kanon (siehe caption_builder.py).",
        f"\n> Story-Teaser (Di 18:00, Motiv {teaser_motiv}): **keine Caption** — Sticker/Tag-Workflow.\n"]
    for p in POSTS:
        md.append(f"\n---\n\n## {H[p]}\n{caps[p]}")
    return "\n".join(md)

if __name__=="__main__":
    # Referenz-Beispiel: Cape Nidhra (kanonische Fassung — „Speichere dir", teile/schicke gemischt)
    hooks={
     "carousel":"Acht Blicke auf ein Suitenhaus am Golf.",
     "vorstellung":"Jede Suite hat ihren eigenen Pool.",
     "ankommen":"Ankommen im Seebad von Hua Hin.",
     "im_detail":"Eigener Pool, warmes Holz, viel Ruhe.",
     "finale":"Wo der Tag am eigenen Pool beginnt."}
    bodies={
     "carousel":("Die Anlage aus der Luft, die Liegen am Hausstrand, der lange Hauptpool, der private Pool "
      "der Nidhrarom-Suite, das Sundeck über dem Meer und die Terrasse des The Rocks: Cape Nidhra direkt am "
      "Strand von Hua Hin, jede Suite mit eigenem Pool. Kein großes Resort, kein Trubel — nur Suiten, Pools und Meer."),
     "vorstellung":("Cape Nidhra steht direkt am Strand von Hua Hin, Thailands ältestem Seebad — ein Haus nur aus "
      "Suiten, und jede hat ihren eigenen Pool. Dazu ein langer Hauptpool zum Meer, ein abgeschirmtes Stück Sand "
      "und die Dachbar On The Rocks über dem Golf. In wenigen Stunden ist Bangkok erreichbar. Kein Inselabenteuer, "
      "kein Trubel — nur Suiten, Pools und Meer."),
     "ankommen":("Hua Hin ist eine Spur gediegener als die lauten Inseln des Südens — geadelt durch den Sommerpalast "
      "der Könige, in Reichweite von Bangkok, ohne Boot, ohne Flug. Cape Nidhra liegt mittendrin und doch "
      "zurückgezogen, zwischen belebter Strandstraße und stillem Sand am Wasser. Man kommt an, und der Ort öffnet "
      "sich ans Meer. Kein weiter Weg, kein Umsteigen — nur Ankommen am Golf."),
     "im_detail":("Cape Nidhra kennt keine gewöhnlichen Zimmer: Jede Einheit ist eine Suite, und jede hat ihren "
      "eigenen Pool. Innen warmes Holz, gedeckte Töne, großzügige Proportionen; der Verzicht auf Dekor ist Absicht "
      "— der Raum selbst soll wirken. Die Krönung ist die Nidhrarom-Suite mit dem längsten Pool und dem offenen "
      "Meer im Blick. Kein Design-Getöse, kein Protz — nur eigener Pool, Holz und Ruhe."),
     "finale":("Du kommst für die Idee — ein Suitenhaus am Strand, in dem jede Suite ihren eigenen Pool hat. Du "
      "bleibst wegen des Rhythmus: Frühstück im Bademantel am eigenen Becken, Bahnen im Salzwasser-Infinity-Pool, "
      "lange Stunden am Strand, und abends kippt das Licht auf der Dachbar On The Rocks über dem Golf von Gold zu "
      "Violett. Kein enges Programm, kein Stillstand — nur der Tag, der am eigenen Pool beginnt.")}
    fragen={
     "carousel":"Swipe durch — bei welchem Bild bleibst du hängen?",
     "vorstellung":"Deluxe Sky Pool Suite oder die weitläufige Nidhrarom — wo würdest du wohnen?",
     "ankommen":"Worauf freust du dich zuerst — Pool, Strand oder das erste Dinner über dem Golf?",
     "im_detail":"Welches Detail würde dich zuerst runterkommen lassen?",
     "finale":"Sky Pool Suite, Strand oder Rooftop — wo würdest du bleiben?"}
    teilen={  # Abwechslung: teile es mit … / schicke es …
     "carousel":"teile es mit deiner Reisecrew",
     "vorstellung":"schicke es deinem Reisebuddy",
     "ankommen":"teile es mit deinem Lieblingsmenschen",
     "im_detail":"schicke es dem Menschen, mit dem du jetzt gern hier wärst",
     "finale":"teile es mit dem Menschen, der dringend ans Meer muss"}
    themen={"carousel":"sehnsuchtsorte","vorstellung":"fernweh","ankommen":"slowtravel",
            "im_detail":"designhotel","finale":"sehnsuchtsorte"}
    caps=build_all("Cape Nidhra","capenidhra","Hua Hin","Thailand",hooks,bodies,fragen,teilen,themen)
    for p in POSTS:
        print("="*8,p,"="*8); print(caps[p]); print()
