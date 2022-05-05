# SteelMP Material

<p>This command is used to construct a uniaxial Menegotto-Pinto steel
material object.</p>

```tcl
uniaxialMaterial SteelMP $matTag $sigmaY $E
        $b
```
<hr />
<table>
<tbody>
<tr class="odd">
<td><p><strong>$matTag</strong></p></td>
<td><p>unique material object integer tag</p></td>
</tr>
<tr class="even">
<td><p><strong>$sigmaY</strong></p></td>
<td><p>yield stress or force</p></td>
</tr>
<tr class="odd">
<td><p><strong>$E</strong></p></td>
<td><p>initial tangent stiffness</p></td>
</tr>
<tr class="even">
<td><p><strong>$b</strong></p></td>
<td><p>strain-hardening ratio (ratio between post-yield tangent and
initial elastic tangent)</p></td>
</tr>
</tbody>
</table>
<p>Note: For this material class, the sensitivity parameters can be:
sigmaY, E, b</p>
<hr />
<dl>
<dt></dt>
<dd>
<dl>
<dt></dt>
<dd>
Reference:
</dd>
<dd>
Barbato M., Conte J.P. (2006). “Finite element structural response
sensitivity and reliability analyses using smooth versus non-smooth
material constitutive models.” International Journal of Reliability and
Safety, 1(1-2):3-39.
</dd>
</dl>
</dd>
</dl>