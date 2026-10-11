"""Make the shapes named rv<k>_* appear on click k (PowerPoint 'Appear' entrance effect).

usage: python3 animate.py deck.pptx
"""
import re
import sys
import zipfile


def timing(groups):
    ids = iter(range(3, 10_000))
    clicks = []
    for k in sorted(groups):
        effects = []
        for j, sp in enumerate(groups[k]):
            node = "clickEffect" if j == 0 else "withEffect"
            a, b = next(ids), next(ids)
            effects.append(
                f'<p:par><p:cTn id="{a}" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="{node}">'
                f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr>'
                f'<p:cTn id="{b}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                f'<p:tgtEl><p:spTgt spid="{sp}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
                f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set></p:childTnLst></p:cTn></p:par>')
        o, i = next(ids), next(ids)
        clicks.append(
            f'<p:par><p:cTn id="{o}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{i}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            + "".join(effects) + '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
    bld = "".join(f'<p:bldP spid="{sp}" grpId="0"/>' for k in sorted(groups) for sp in groups[k])
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            + "".join(clicks) +
            '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
            f'</p:childTnLst></p:cTn></p:par></p:tnLst><p:bldLst>{bld}</p:bldLst></p:timing>')


def main(path):
    zin = zipfile.ZipFile(path)
    items = [(i, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    n = 0
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", info.filename):
                xml = data.decode("utf-8")
                groups = {}
                for sp, k in re.findall(r'<p:cNvPr id="(\d+)" name="rv(\d+)_\d+"', xml):
                    groups.setdefault(int(k), []).append(sp)
                if groups:
                    assert "<p:timing>" not in xml
                    xml = xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + timing(groups), 1)
                    assert "<p:timing>" in xml, info.filename
                    data = xml.encode("utf-8"); n += 1
            z.writestr(info, data)
    print(f"animated {n} slides")


if __name__ == "__main__":
    main(sys.argv[1])
