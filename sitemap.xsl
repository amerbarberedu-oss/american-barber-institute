<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:sm="http://www.sitemaps.org/schemas/sitemap/0.9">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html>
<head>
<title>XML Sitemap — American Barber Institute</title>
<meta name="robots" content="noindex"/>
<style>
  body{font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;color:#333;margin:40px auto;max-width:1000px;padding:0 24px;background:#fff}
  h1{font-size:2.1rem;color:#4a4a4a;margin:0 0 18px}
  p.meta{color:#555;margin:.35em 0}
  a{color:#a87900;text-decoration:none}
  a:hover{text-decoration:underline}
  table{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:18px}
  th{text-align:left;border-bottom:2px solid #d9d9d9;padding:9px 12px;color:#444}
  td{padding:9px 12px}
  tr:nth-child(even) td{background:#f2f2f2}
</style>
</head>
<body>
<h1>XML Sitemap</h1>
<p class="meta">Generated for <strong>American Barber Institute</strong>, this is an XML Sitemap, meant for consumption by search engines.</p>
<p class="meta">You can find more information about XML sitemaps on <a href="https://www.sitemaps.org">sitemaps.org</a>.</p>
<xsl:choose>
  <xsl:when test="sm:sitemapindex">
    <p class="meta">This XML Sitemap Index file contains <strong><xsl:value-of select="count(sm:sitemapindex/sm:sitemap)"/></strong> sitemaps.</p>
    <table>
      <tr><th>Sitemap</th><th>Last Modified</th></tr>
      <xsl:for-each select="sm:sitemapindex/sm:sitemap">
        <tr>
          <td><a href="{sm:loc}"><xsl:value-of select="sm:loc"/></a></td>
          <td><xsl:value-of select="sm:lastmod"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:when>
  <xsl:otherwise>
    <p class="meta">This XML Sitemap contains <strong><xsl:value-of select="count(sm:urlset/sm:url)"/></strong> URLs.</p>
    <table>
      <tr><th>URL</th><th>Priority</th><th>Change Freq.</th><th>Last Mod.</th></tr>
      <xsl:for-each select="sm:urlset/sm:url">
        <tr>
          <td><a href="{sm:loc}"><xsl:value-of select="sm:loc"/></a></td>
          <td><xsl:value-of select="sm:priority"/></td>
          <td><xsl:value-of select="sm:changefreq"/></td>
          <td><xsl:value-of select="sm:lastmod"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:otherwise>
</xsl:choose>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
