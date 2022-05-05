# Standard Brick Element

<p>This element is used to construct an eight-node brick element object,
which uses a trilinear isoparametric formulation.</p>
<table>
<tbody>
<tr class="odd">
<td><p><strong>element stdBrick $eleTag $node1 $node2 $node3 $node4
$node5 $node6 $node7 $node8 $matTag &lt;$b1 $b2
$b3&gt;</strong></p></td>
</tr>
</tbody>
</table>
<hr />
<table>
<tbody>
<tr class="odd">
<td><p><strong>$eleTag</strong></p></td>
<td><p>unique element object tag</p></td>
</tr>
<tr class="even">
<td><p><strong>$node1 $node2</strong></p>
<p><strong>$node3 $node4</strong></p>
<p><strong>$node5 $node6</strong></p>
<p><strong>$node7 $node8</strong></p></td>
<td><p>eight nodes defining element boundaries, input order is shown in
the figure.</p></td>
</tr>
<tr class="odd">
<td><p><strong>$matTag</strong></p></td>
<td><p>tag of nDMaterial</p></td>
</tr>
<tr class="even">
<td><p><strong>'$b1 $b2 $b3</strong></p></td>
<td><p>body forces in global x,y,z directions</p></td>
</tr>
</tbody>
</table>
<figure>
<img src="Brick.gif" title="Brick.gif" alt="Brick.gif" />
<figcaption aria-hidden="true">Brick.gif</figcaption>
</figure>
<p>NOTE:</p>
<ol>
<li>The valid queries to a Brick element when creating an
ElementRecorder object are 'forces', 'stresses,' ('strains' version &gt;
2.2.0) and 'material $matNum matArg1 matArg2 ...' Where $matNum refers
to the material object at the integration point corresponding to the
node numbers in the isoparametric domain.</li>
<li>This element can only be defined in -ndm 3 -ndf 3</li>
</ol>
<p>EXAMPLE:</p>
<p>REFERENCES:</p>
<hr />
<p>Code Developed by: <span style="color:blue"> Edward Love,
Sandia National Laboratories </span></p>